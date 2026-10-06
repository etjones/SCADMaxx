#requires -Version 7.2
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Source, [switch]$CheckOnly)
$ErrorActionPreference='Stop'
$Source=(Resolve-Path -LiteralPath $Source).Path.Replace('\','/')
$patch=Join-Path $PSScriptRoot '../patches/feature-build-title.patch'
$gitArgs=@('-c',"safe.directory=$Source",'-C',$Source)
& git @gitArgs rev-parse --show-toplevel | Out-Null
if($LASTEXITCODE -ne 0){throw 'Source must be a Git checkout'}
& git @gitArgs apply --reverse --check $patch 2>$null
if($LASTEXITCODE -eq 0){Write-Output 'Feature title patch is already applied.';exit 0}
& git @gitArgs apply --check $patch
if($LASTEXITCODE -ne 0){throw 'Patch does not apply cleanly. Preserve local changes and update the central patch; do not invent a branch-specific variant.'}
if($CheckOnly){Write-Output 'Feature title patch applies cleanly.';exit 0}
& git @gitArgs apply $patch
if($LASTEXITCODE -ne 0){throw 'Patch application failed'}
Write-Output 'Applied feature title patch. Reconfigure/build normally; Git identity is embedded at configure time.'
