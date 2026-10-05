[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$BuildDirectory,
    [Parameter(Mandatory)][string]$OutputDirectory,
    [string]$Configuration = 'Release'
)
$ErrorActionPreference = 'Stop'
function Invoke-Checked([string]$Command, [string[]]$Arguments) {
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Command failed with exit code $LASTEXITCODE" }
}
$version = & (Join-Path $PSScriptRoot 'Get-Version.ps1')
$versionHash = (Get-FileHash (Join-Path $PSScriptRoot 'version.xml')).Hash
$BuildDirectory = [IO.Path]::GetFullPath($BuildDirectory)
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
if (!(Test-Path (Join-Path $BuildDirectory 'CMakeCache.txt'))) {
    throw 'Configure the build directory first; see BUILDING.md.'
}
$name = "scadmaxx-launcher-$version"
$stage = Join-Path $OutputDirectory $name
$archive = "$stage.zip"
if ((Test-Path -LiteralPath $stage) -or (Test-Path -LiteralPath $archive)) {
    throw "Release output already exists: $stage or $archive. Choose another output parent; never bump the version to avoid a collision."
}
# Reconfigure to consume the current XML even when reusing an older build directory.
Invoke-Checked 'cmake' @('-S', $PSScriptRoot, '-B', $BuildDirectory, '-DBUILD_TESTING=ON')
Invoke-Checked 'cmake' @('--build', $BuildDirectory, '--config', $Configuration)
Invoke-Checked 'ctest' @('--test-dir', $BuildDirectory, '-C', $Configuration, '--output-on-failure', '--no-tests=error')
if ((Get-FileHash (Join-Path $PSScriptRoot 'version.xml')).Hash -ne $versionHash) {
    throw 'version.xml changed during the build; retry with a stable source state.'
}
New-Item -ItemType Directory -Path $stage | Out-Null
Invoke-Checked 'cmake' @('--install', $BuildDirectory, '--config', $Configuration, '--prefix', $stage)
Push-Location $stage
try { Invoke-Checked 'cmake' @('-E', 'tar', 'cf', $archive, '--format=zip', '--', '.') }
finally { Pop-Location }
Write-Host "Created $stage"
Write-Host "Created $archive"
