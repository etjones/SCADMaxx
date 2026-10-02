#requires -Version 7.2
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
. "$PSScriptRoot/Common.ps1"
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../runs/tool-tests'))
New-Item -ItemType Directory -Force $root | Out-Null
$case = Join-Path $root ([Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory $case | Out-Null
$script:LogPath = Join-Path $case 'commands.log'
$script:CommandRecords = [Collections.Generic.List[object]]::new()
$pwsh = (Get-Command pwsh).Source
$count = 0
function Expect-Failure([scriptblock]$Action, [string]$Pattern) {
    try { & $Action } catch { if ($_.ToString() -notmatch $Pattern) { throw }; return }
    throw "Expected failure matching $Pattern"
}
Assert-ChildPath (Join-Path $root 'child') $root
Expect-Failure { Assert-ChildPath "$root-other/child" $root } 'Path must be inside'
$count++
Invoke-Logged $pwsh @('-NoProfile','-Command','Write-Output "captured output"; exit 0')
if ((Get-Content $script:LogPath -Raw) -notmatch 'captured output') { throw 'Output was not captured.' }
$count++
Expect-Failure { Invoke-Logged $pwsh @('-NoProfile','-Command','Write-Error "expected failure"; exit 7') } 'exit code 7'
if ($script:CommandRecords[1].exitCode -ne 7) { throw 'Native failure was not preserved.' }
$count++
Expect-Failure {
    Invoke-Logged $pwsh @('-NoProfile','-Command','Write-Output "ERROR: missing shader"; exit 0') -RejectErrors
} 'reported errors despite exit code zero'
$count++
if ((Get-TextHash 'stable') -ne (Get-TextHash 'stable') -or (Get-TextHash 'stable') -eq (Get-TextHash 'changed')) {
    throw 'Fingerprint hashing failed.'
}
$count++
$inventoryDir = Join-Path $case 'inventory'
New-Item -ItemType Directory $inventoryDir | Out-Null
Set-Content (Join-Path $inventoryDir 'file.txt') 'before'
$before = @(Get-FileInventory $inventoryDir)
Set-Content (Join-Path $inventoryDir 'file.txt') 'after'
$after = @(Get-FileInventory $inventoryDir)
if ($before[0].sha256 -eq $after[0].sha256) { throw 'Staging content modification was not detected.' }
$count++
Expect-Failure { & "$PSScriptRoot/New-ExperimentalRun.ps1" -RunId '../invalid' } 'Run ID must contain'
$count++
New-Item -ItemType Directory -Force (Join-Path $case 'runs/existing') | Out-Null
Expect-Failure { & "$PSScriptRoot/New-ExperimentalRun.ps1" -Workspace $case -ControlRoot $case -RunId 'existing' } 'Run or worktree already exists'
$count++
$fixtureRepo = Join-Path $case 'openscad-master'
Invoke-Logged 'git' @('init','-b','main',$fixtureRepo)
Invoke-Logged 'git' @('-C',$fixtureRepo,'remote','add','upstream','https://github.com/openscad/openscad.git')
New-Item -ItemType Directory (Join-Path $case 'experimental') | Out-Null
'{}' | Set-Content (Join-Path $case 'experimental/SOURCES.json')
@'
## Enabled stack (ordered)

| Order | ID | Kind | Source | Revision | Delta base | Depends on | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | first | pr | https://github.com/openscad/openscad/pull/6878 | latest | auto-merge-base | none declared | Test fixture |
| 2 | second | pr | https://github.com/openscad/openscad/pull/6776 | latest | auto-merge-base | none declared | Test fixture |

## Candidates
| 3 | unselected | pr | https://github.com/openscad/openscad/pull/6871 | latest | auto-merge-base | none declared | Must stay unselected |
'@ | Set-Content (Join-Path $case 'experimental/PR_STACK.md')
$selected = & "$PSScriptRoot/New-ExperimentalRun.ps1" -Workspace $case -ControlRoot $case -RunId 'validation' -ValidateOnly | ConvertFrom-Json
if ($selected.Count -ne 2 -or $selected[0].id -ne 'first' -or $selected[1].dependencies.Count -ne 0) {
    throw 'Enabled selection parsing failed or included an unselected candidate.'
}
if (Test-Path (Join-Path $case 'runs/validation')) { throw 'Read-only validation created a run.' }
$count++
@'
## Enabled stack (ordered)
| Order | ID | Kind | Source | Revision | Delta base | Depends on | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | local-feature | feature | local-feature | latest | auto-merge-base | none declared | Required unfinished feature |
'@ | Set-Content (Join-Path $case 'experimental/PR_STACK.md')
$featureDefinition = @{'local-feature'=@{repository='D:/nonexistent-selected-feature.git';
    ref='refs/heads/feature/example'; ready=$false; pendingReason='Implementation is not committed yet.'}}
Save-Json (Join-Path $case 'experimental/SOURCES.json') $featureDefinition
$selected = & "$PSScriptRoot/New-ExperimentalRun.ps1" -Workspace $case -ControlRoot $case -RunId 'pending-feature' -ValidateOnly | ConvertFrom-Json
if ($selected.ready -ne $false -or !$selected.pendingReason) { throw 'Validation lost pending feature state.' }
Expect-Failure { & "$PSScriptRoot/New-ExperimentalRun.ps1" -Workspace $case -ControlRoot $case -RunId 'pending-feature' } 'Selected features are not ready'
if (Test-Path (Join-Path $case 'runs/pending-feature')) { throw 'Pending feature created a run.' }
if (Read-Git $fixtureRepo @('for-each-ref','--format=%(refname)')) { throw 'Pending feature changed Git refs.' }
$count++
$featureDefinition['local-feature'].ready = 'false'
Save-Json (Join-Path $case 'experimental/SOURCES.json') $featureDefinition
Expect-Failure { & "$PSScriptRoot/New-ExperimentalRun.ps1" -Workspace $case -ControlRoot $case -RunId 'invalid-ready' -ValidateOnly } 'JSON boolean'
$count++
$featureDefinition['local-feature'].ready = $true
Save-Json (Join-Path $case 'experimental/SOURCES.json') $featureDefinition
$selected = & "$PSScriptRoot/New-ExperimentalRun.ps1" -Workspace $case -ControlRoot $case -RunId 'ready-feature' -ValidateOnly | ConvertFrom-Json
if (!$selected.ready) { throw 'Ready feature remained pending.' }
$count++
$testSource = Join-Path $case 'generated-header-fixture'
$clipper = Join-Path $testSource 'submodules/Clipper2'
$relative = 'CPP/Clipper2Lib/include/clipper2/clipper.version.h'
$header = Join-Path $clipper $relative
Assert-ChildPath $clipper $case
New-Item -ItemType Directory -Force (Split-Path $header) | Out-Null
Invoke-Logged 'git' @('init','-b','main',$clipper)
Invoke-Logged 'git' @('-C',$clipper,'config','core.autocrlf','true')
[IO.File]::WriteAllText($header,"fixture`n")
Invoke-Logged 'git' @('-C',$clipper,'add','--',$relative)
# This commit belongs only to a newly created disposable test repository under runs/tool-tests.
$emptyHooks = Join-Path $case 'empty-hooks'
New-Item -ItemType Directory $emptyHooks | Out-Null
Invoke-Logged 'git' @('-C',$clipper,'-c','user.name=Build tool fixture','-c','user.email=fixture@example.invalid',
    '-c',"core.hooksPath=$emptyHooks",'-c','commit.gpgsign=false','commit','-m','Create generated-header test fixture')
Invoke-Logged 'git' @('-C',$clipper,'checkout-index','--index','--force','--',$relative)
[IO.File]::WriteAllText($header,"fixture`n")
Refresh-ClipperGeneratedHeader $testSource
if (Read-Git $clipper @('status','--porcelain')) { throw 'Content-identical generated header remained dirty.' }
$count++
$originalIndex = Read-Git $clipper @('rev-parse',":$relative")
[IO.File]::WriteAllText($header,"real content change`n")
Expect-Failure { Refresh-ClipperGeneratedHeader $testSource } 'real source change'
if ((Read-Git $clipper @('rev-parse',":$relative")) -ne $originalIndex -or
    (Get-Content $header -Raw) -ne "real content change`n") { throw 'A real change was staged or overwritten.' }
$count++
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$names = Get-IntegrationNames $case $clipper '20261002'
if ($names.branch -ne 'scadmaxx-20261002' -or
    $names.source -ne (Join-Path $case 'wt-scadmaxx-20261002')) { throw 'Date-based naming failed.' }
New-Item -ItemType Directory $names.source | Out-Null
Invoke-Logged 'git' @('-C',$clipper,'update-ref','refs/heads/scadmaxx-20261002-2','HEAD')
Invoke-Logged 'git' @('-C',$clipper,'update-ref','refs/remotes/origin/scadmaxx-20261002-3','HEAD')
$names = Get-IntegrationNames $case $clipper '20261002'
if ($names.branch -ne 'scadmaxx-20261002-4' -or
    $names.source -ne (Join-Path $case 'wt-scadmaxx-20261002-4')) {
    throw 'Directory/local/remote naming collision was not preserved.'
}
$count++
$container = Split-Path $workspace -Parent
Assert-ChildPath $case (Join-Path $container 'runs')
if (!(Test-Path (Join-Path $workspace 'experimental/PR_STACK.md')) -or
    !(Test-Path (Join-Path $container 'openscad-master/.git'))) { throw 'Separated control/container layout failed.' }
$count++
$snapshotRun = Join-Path $case 'snapshot-run'
New-Item -ItemType Directory $snapshotRun | Out-Null
Save-Json (Join-Path $snapshotRun 'inputs.json') @{source='D:/old-checkout'; branch='experimental/old'; upstream='fixed'}
$inputHash = (Get-FileHash (Join-Path $snapshotRun 'inputs.json')).Hash
$overlay = @{inputsSha256=$inputHash; oldSource='D:/old-checkout'; oldBranch='experimental/old';
    source=(Join-Path $case 'wt-scadmaxx-20261002'); branch='scadmaxx-20261002'}
Save-Json (Join-Path $snapshotRun 'layout-migration.json') $overlay
$resolved = Read-RunInputs $snapshotRun
if ($resolved.branch -ne 'scadmaxx-20261002' -or $resolved.upstream -ne 'fixed' -or
    (Get-FileHash (Join-Path $snapshotRun 'inputs.json')).Hash -ne $inputHash) { throw 'Migration altered frozen inputs.' }
$overlay.inputsSha256 = 'wrong'
Save-Json (Join-Path $snapshotRun 'layout-migration.json') $overlay
Expect-Failure { Read-RunInputs $snapshotRun } 'does not match frozen'
$count++
'# Frozen test selection' | Set-Content (Join-Path $snapshotRun 'PR_STACK.md')
'{"frozenTestSource":true}' | Set-Content (Join-Path $snapshotRun 'source-definitions.json')
$snapshot = Save-ControlSnapshot $workspace $snapshotRun 'test' ''
$snapshotInfo = Get-Content (Join-Path $snapshot 'snapshot.json') -Raw | ConvertFrom-Json
foreach ($relative in @('workflows/update-and-build-scadmaxx.md','docs/git-layout.md','docs/worktrees.md',
    'experimental/templates/run-report.md')) {
    $copiedPath = Join-Path $snapshot $relative
    if (!(Test-Path -LiteralPath $copiedPath) -or
        (Get-FileHash $copiedPath).Hash -ne (Get-FileHash (Join-Path $workspace $relative)).Hash) {
        throw "Build snapshot omitted or changed an instruction input: $relative"
    }
    $record = @($snapshotInfo.files | Where-Object { $_.path.Replace('\','/') -eq $relative })
    if ($record.Count -ne 1 -or $record[0].sha256 -ne (Get-FileHash $copiedPath).Hash) {
        throw "Instruction input hash missing from snapshot inventory: $relative"
    }
}
if ((Get-Content (Join-Path $snapshot 'experimental/PR_STACK.md') -Raw).Trim() -ne '# Frozen test selection' -or
    !(Get-Content (Join-Path $snapshot 'experimental/SOURCES.json') -Raw | ConvertFrom-Json).frozenTestSource) {
    throw 'Build snapshot used live selection files instead of frozen inputs.'
}
$count++
Save-Json (Join-Path $case 'evidence.json') @{commands=@($script:CommandRecords.ToArray()); casesPassed=$count}
"Passed $count build-tool checks. Evidence: $case"
