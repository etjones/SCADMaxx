#requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$BuildDirectory,
    [string]$Profile = (Join-Path $PSScriptRoot '../profiles/this-machine.local.json'),
    [int]$Parallel = 3
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$machine = Get-Content -LiteralPath $Profile -Raw | ConvertFrom-Json
$BuildDirectory = (Resolve-Path -LiteralPath $BuildDirectory).Path
if (!(Test-Path -LiteralPath (Join-Path $BuildDirectory 'CMakeCache.txt'))) {
    throw 'Configure the feature build with the documented shared dependency profile first.'
}
Import-Module (Join-Path $machine.visualStudio 'Common7/Tools/Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $machine.visualStudio -Arch amd64 -HostArch amd64 -SkipAutomaticLocation `
    -DevCmdArguments "-vcvars_ver=$($machine.toolset) -winsdk=$($machine.sdk)" | Out-Null
$triplet = Join-Path $machine.vcpkgInstalled 'x64-windows'
$env:PATH = "$triplet/bin;$triplet/tools/gettext/bin;C:/Program Files/Git/usr/bin;$env:PATH"

# Qt UI headers can change class layout. Finish generation before Ninja evaluates
# the application's existing object dependencies, including indirect UI consumers.
& $machine.cmake --build $BuildDirectory --config Release --target OpenSCADLibInternal_autogen --parallel $Parallel
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $machine.cmake --build $BuildDirectory --config Release --target OpenSCADExe winconsole --parallel $Parallel
exit $LASTEXITCODE
