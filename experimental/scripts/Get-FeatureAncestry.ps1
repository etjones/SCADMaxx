#requires -Version 7.2
[CmdletBinding()]
param(
    [string]$Workspace = ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))),
    [string]$ControlRoot = ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..')))
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
. "$PSScriptRoot/Common.ps1"
$repo = Join-Path $Workspace 'openscad-master'
$manifest = Get-Content (Join-Path $ControlRoot 'experimental/DEPENDENCIES.json') -Raw | ConvertFrom-Json -AsHashtable
$sources = Get-Content (Join-Path $ControlRoot 'experimental/SOURCES.json') -Raw | ConvertFrom-Json -AsHashtable
function Contains-Revision([string]$Ancestor, [string]$Head) {
    & git -C $repo merge-base --is-ancestor $Ancestor $Head
    if ($LASTEXITCODE -notin @(0,1)) { throw "Cannot inspect ancestry: $Ancestor -> $Head" }
    return $LASTEXITCODE -eq 0
}
$report = foreach ($id in ($manifest.nodes.Keys | Sort-Object)) {
    $node = $manifest.nodes[$id]
    $head = if ($node.ContainsKey('ref')) { Read-Git $repo @('rev-parse',$node.ref) } else { $node.acceptedHead }
    $source = if ($node.ContainsKey('sourceKey')) { $sources[$node.sourceKey] } else { @{} }
    $dependencies = foreach ($dependency in ($node.dependencies.Keys | Sort-Object)) {
        $owner = $manifest.nodes[$dependency]
        $available = if ($owner.ContainsKey('ref')) { Read-Git $repo @('rev-parse',$owner.ref) } else { $owner.acceptedHead }
        @{
            id=$dependency; accepted=$node.dependencies[$dependency]; availableLocal=$available
            acceptedIsAncestor=(Contains-Revision $node.dependencies[$dependency] $head)
            availableIsAncestor=(Contains-Revision $available $head)
        }
    }
    @{
        id=$id; accepted=$node.acceptedHead; availableLocal=$head
        acceptedMatchesLocal=($head -eq $node.acceptedHead)
        promoted=$source['promotedHead']; validated=$source['validatedHead']; ready=$source['ready']
        dependencies=@($dependencies)
    }
}
$report | ConvertTo-Json -Depth 10
