#requires -Version 7.2
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Source)
$ErrorActionPreference='Stop'
$PSNativeCommandUseErrorActionPreference=$false
$Source=(Resolve-Path -LiteralPath $Source).Path.Replace('\','/')
$patch=Join-Path $PSScriptRoot '../patches/scadmaxx-icon.patch'
$gitArgs=@('-c',"safe.directory=$Source",'-C',$Source)
& git @gitArgs rev-parse --show-toplevel | Out-Null
if($LASTEXITCODE -ne 0){throw 'Source must be a Git checkout'}
& git @gitArgs apply --reverse --check $patch 2>$null
if($LASTEXITCODE -eq 0){Write-Output 'SCADMaxx icon patch is already applied.';exit 0}
& git @gitArgs apply --check $patch
if($LASTEXITCODE -ne 0){throw 'Icon patch conflicts with this checkout. Preserve its assets; reconcile the canonical patch rather than silently overwriting changes.'}
& git @gitArgs apply $patch
if($LASTEXITCODE -ne 0){throw 'Icon patch application failed'}
Write-Output 'Applied purple SCADMaxx icons. Existing executables change only after an explicitly requested rebuild.'
