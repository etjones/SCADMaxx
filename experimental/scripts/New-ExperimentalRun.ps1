#requires -Version 7.2
[CmdletBinding()]
param(
    [string]$Workspace = ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))),
    [string]$RunId = (Get-Date -AsUTC -Format yyyyMMddTHHmmssZ),
    [string]$SourceDefinitions,
    [switch]$ValidateOnly
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
. "$PSScriptRoot/Common.ps1"
if ($RunId -notmatch '^[A-Za-z0-9][A-Za-z0-9-]*$') { throw 'Run ID must contain only letters, digits, and hyphens.' }
$Workspace = [IO.Path]::GetFullPath($Workspace)
$repo = Join-Path $Workspace 'openscad-master'
$run = Join-Path $Workspace "runs/$RunId"
$source = Join-Path $Workspace "wt-openscad-experimental-$RunId"
$branch = "experimental/$RunId"
if ((Test-Path $run) -or (Test-Path $source)) { throw 'Run or worktree already exists. Resume its frozen inputs instead.' }
if ((Read-Git $repo @('remote','get-url','upstream')) -ne 'https://github.com/openscad/openscad.git') {
    throw 'Unexpected upstream remote; verify it before fetching.'
}
if (Read-Git $repo @('for-each-ref','--format=%(refname)',"refs/experimental-runs/$RunId/","refs/heads/$branch")) {
    throw 'This run ID already owns retained refs or a branch. Resume it or choose a new ID.'
}
$stack = Get-Content (Join-Path $Workspace 'experimental/PR_STACK.md') -Raw
$section = [regex]::Match($stack,'(?ms)^## Enabled stack[^\r\n]*\r?\n(.*?)(?=^## |\z)').Groups[1].Value
$rows = @($section -split '\r?\n' | Where-Object { $_ -match '^\|\s*\d+\s*\|' })
if (!$rows.Count) { throw 'No entries enabled; an enhanced build requires an explicit selection.' }
if (!$SourceDefinitions) { $SourceDefinitions = Join-Path $Workspace 'experimental/SOURCES.json' }
$definitions = Get-Content $SourceDefinitions -Raw | ConvertFrom-Json -AsHashtable
$ids = @()
$orders = @()
$entries = foreach ($row in $rows) {
    $cells = @($row.Trim().Trim('|').Split('|') | ForEach-Object { $_.Trim() })
    if ($cells.Count -ne 8) { throw "Expected eight selection columns: $row" }
    $order,$id,$kind,$selectedSource,$revision,$deltaBase,$depends,$reason = $cells
    if ($id -notmatch '^[a-z0-9][a-z0-9-]*$' -or $id -in $ids -or [int]$order -in $orders) { throw 'Invalid/duplicate selection ID or order.' }
    if ($orders.Count -and [int]$order -le $orders[-1]) { throw 'Rows must be in ascending order; do not silently reorder.' }
    $dependencies = @(if ($depends -ne 'none declared') { $depends.Split(',') | ForEach-Object { $_.Trim() } })
    foreach ($dependency in $dependencies) { if ($dependency -notin $ids) { throw "Dependency $dependency must be selected earlier." } }
    if ($dependencies.Count -and $deltaBase -eq 'auto-merge-base') { throw "Stacked entry $id needs an explicit delta base." }
    if ($revision -ne 'latest' -and $revision -notmatch '^[0-9a-f]{40}$') { throw "Invalid revision for $id" }
    if ($deltaBase -ne 'auto-merge-base' -and $deltaBase -notmatch '^[0-9a-f]{40}$') { throw "Invalid delta base for $id" }
    $ready = $true
    $pendingReason = $null
    if ($kind -eq 'pr') {
        if ($selectedSource -notmatch '^https://github.com/openscad/openscad/pull/(\d+)$') { throw 'Expected an OpenSCAD PR URL.' }
        $number = $Matches[1]
        $repository = 'https://github.com/openscad/openscad.git'
        $ref = "refs/pull/$number/head"
        $prUrl = $selectedSource
    } elseif ($kind -in @('feature','pr-variant')) {
        if (!$definitions.ContainsKey($selectedSource)) { throw "Missing explicit source definition: $selectedSource" }
        $definition = $definitions[$selectedSource]
        if ($definition.ContainsKey('ready')) {
            if ($definition.ready -isnot [bool]) { throw "Source readiness must be a JSON boolean: $selectedSource" }
            $ready = $definition.ready
        }
        if (!$ready) {
            $pendingReason = $definition.pendingReason
            if ([string]::IsNullOrWhiteSpace($pendingReason)) { throw "Pending source needs a reason: $selectedSource" }
        }
        $repository = $definition.repository
        $ref = $definition.ref
        if (!$repository -or $ref -notmatch '^refs/(heads|tags)/') { throw 'Source definitions need repository and full ref.' }
        $prUrl = if ($kind -eq 'pr-variant') { $definition.prUrl } else { $null }
        if ($kind -eq 'pr-variant' -and $prUrl -notmatch '^https://github.com/openscad/openscad/pull/\d+$') { throw 'Variant needs its original PR URL.' }
    } else { throw "Unknown source kind: $kind" }
    $ids += $id
    $orders += [int]$order
    @{id=$id; order=[int]$order; kind=$kind; repository=$repository; sourceRef=$ref; revision=$revision;
      deltaBase=$deltaBase; dependencies=$dependencies; reason=$reason; prUrl=$prUrl;
      ready=$ready; pendingReason=$pendingReason}
}
if ($ValidateOnly) {
    $entries | ConvertTo-Json -Depth 10
    return
}
$pending = @($entries | Where-Object { !$_.ready })
if ($pending.Count) {
    $details = ($pending | ForEach-Object { "$($_.id): $($_.pendingReason)" }) -join '; '
    throw "Selected features are not ready for integration: $details"
}
New-Item -ItemType Directory -Path $run,(Join-Path $run 'logs') | Out-Null
$script:LogPath = Join-Path $run 'logs/prepare.log'
$script:CommandRecords = [Collections.Generic.List[object]]::new()
$info = [ordered]@{runId=$RunId; versionDate=(Get-Date -AsUTC -Format yyyy.MM.dd); status='preparing'; source=$source; branch=$branch; entries=@($entries)}
try {
    Copy-Item (Join-Path $Workspace 'experimental/PR_STACK.md') (Join-Path $run 'PR_STACK.md')
    Copy-Item (Join-Path $Workspace 'experimental/templates/run-report.md') (Join-Path $run 'report.md')
    if ($SourceDefinitions) { Copy-Item $SourceDefinitions (Join-Path $run 'source-definitions.json') }
    $info.controlSnapshot = Save-ControlSnapshot $Workspace $run 'prepare' ''
    Invoke-Logged 'git' @('-C',$repo,'fetch','upstream',"refs/heads/master:refs/experimental-runs/$RunId/upstream")
    $info.upstream = Read-Git $repo @('rev-parse',"refs/experimental-runs/$RunId/upstream")
    foreach ($entry in $entries) {
        $retained = "refs/experimental-runs/$RunId/$($entry.id)"
        Invoke-Logged 'git' @('-C',$repo,'fetch',$entry.repository,"$($entry.sourceRef):$retained-tip")
        $tip = Read-Git $repo @('rev-parse',"$retained-tip^{commit}")
        $entry.head = if ($entry.revision -eq 'latest') { $tip } else { $entry.revision }
        Invoke-Logged 'git' @('-C',$repo,'merge-base','--is-ancestor',$entry.head,$tip)
        Invoke-Logged 'git' @('-C',$repo,'update-ref',$retained,$entry.head)
        $entry.retainedRef = $retained
        if ($entry.deltaBase -eq 'auto-merge-base') {
            $bases = (Read-Git $repo @('merge-base','--all',$info.upstream,$entry.head)) -split '\n'
            if ($bases.Count -ne 1) { throw "Ambiguous merge base for $($entry.id)" }
            $entry.deltaBase = $bases[0]
        }
        Invoke-Logged 'git' @('-C',$repo,'merge-base','--is-ancestor',$entry.deltaBase,$entry.head)
        if ($entry.prUrl) {
            $number = $entry.prUrl.Split('/')[-1]
            $pr = Invoke-RestMethod "https://api.github.com/repos/openscad/openscad/pulls/$number"
            $entry.prState = $pr.state
            $entry.prMerged = $pr.merged
            $entry.originalPrHead = $pr.head.sha
        }
        $patch = Join-Path $run "$($entry.id).patch"
        Invoke-Logged 'git' @('-C',$repo,'diff','--binary',"--output=$patch",$entry.deltaBase,$entry.head)
        $entry.patchSha256 = (Get-FileHash $patch).Hash
        Read-Git $repo @('log','--format=fuller',"$($entry.deltaBase)..$($entry.head)") |
            Set-Content (Join-Path $run "$($entry.id)-commits.txt")
    }
    $info.stackSha256 = (Get-FileHash (Join-Path $run 'PR_STACK.md')).Hash
    Save-Json (Join-Path $run 'inputs.json') $info
    Invoke-Logged 'git' @('-C',$repo,'worktree','add','--no-track','-b',$branch,$source,$info.upstream)
    Invoke-Logged 'git' @('-C',$source,'config',"branch.$branch.pushRemote",'origin')
    Invoke-Logged 'git' @('-C',$source,'submodule','update','--init','--recursive')
    $info.status = 'prepared-not-integrated'
    Write-Output "Prepared $source. Build the baseline, then review/apply each frozen delta with separate integration and repair commits."
} catch {
    $info.status = 'prepare-failed'
    $info.error = $_.ToString()
    throw
} finally {
    Save-Json (Join-Path $run 'inputs.json') $info
    Save-Json (Join-Path $run 'logs/prepare-commands.json') @($script:CommandRecords.ToArray())
}
