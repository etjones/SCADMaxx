#requires -Version 7.2
param([Parameter(Mandatory)][string]$BuildProfile)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
. "$PSScriptRoot/Common.ps1"
$p = Get-Content -LiteralPath $BuildProfile -Raw | ConvertFrom-Json -AsHashtable
$dependencies = Get-SharedVcpkgConfiguration $p
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../runs/tool-tests'))
$case = Join-Path $root ("shared-vcpkg-" + [Guid]::NewGuid().ToString('N'))
$source = Join-Path $case 'source'
$build = Join-Path $case 'build'
New-Item -ItemType Directory -Force $source | Out-Null
$identityProbe = Join-Path $case 'dependency-identity.ps1'
@'
param([string]$Common, [string]$ProfilePath)
. $Common
$profileData = Get-Content -LiteralPath $ProfilePath -Raw | ConvertFrom-Json -AsHashtable
$configuration = Get-SharedVcpkgConfiguration $profileData
if ($configuration -isnot [Collections.Specialized.OrderedDictionary]) { throw 'Dependency identity must have stable key order.' }
Get-TextHash ($configuration | ConvertTo-Json -Depth 20 -Compress)
'@ | Set-Content $identityProbe -Encoding utf8NoBOM
$expectedIdentity = Get-TextHash ($dependencies | ConvertTo-Json -Depth 20 -Compress)
foreach ($attempt in 1..3) {
    $actualIdentity = & (Get-Command pwsh).Source -NoProfile -File $identityProbe -Common "$PSScriptRoot/Common.ps1" -ProfilePath $BuildProfile
    if ($LASTEXITCODE -or $actualIdentity -ne $expectedIdentity) { throw 'Dependency identity changed between PowerShell processes.' }
}
$script:LogPath = Join-Path $case 'commands.log'
$script:CommandRecords = [Collections.Generic.List[object]]::new()
@'
cmake_minimum_required(VERSION 3.25)
project(SharedDependencyCheck LANGUAGES NONE)
if(VCPKG_MANIFEST_MODE OR VCPKG_MANIFEST_INSTALL)
  message(FATAL_ERROR "Automatic dependency installation is enabled")
endif()
find_library(SHARED_QT_CORE NAMES Qt6Core REQUIRED)
file(REAL_PATH "${VCPKG_INSTALLED_DIR}/x64-windows/lib" expected)
cmake_path(IS_PREFIX expected "${SHARED_QT_CORE}" NORMALIZE from_shared)
if(NOT from_shared)
  message(FATAL_ERROR "Qt library did not come from the selected shared installation")
endif()
message(STATUS "Using shared Qt: ${SHARED_QT_CORE}")
'@ | Set-Content (Join-Path $source 'CMakeLists.txt') -Encoding utf8NoBOM
# If manifest installation were enabled, this deliberately unresolvable dependency would fail configure.
'{"name":"no-install-fixture","version":"1.0.0","dependencies":["must-never-install-this-fixture"]}' |
    Set-Content (Join-Path $source 'vcpkg.json') -Encoding utf8NoBOM
$ninja = Join-Path $p.visualStudio 'Common7/IDE/CommonExtensions/Microsoft/CMake/Ninja/ninja.exe'
$arguments = @('-S',$source,'-B',$build,'-G','Ninja',"-DCMAKE_MAKE_PROGRAM=$ninja",
    "-DCMAKE_TOOLCHAIN_FILE=$($p.vcpkg)/scripts/buildsystems/vcpkg.cmake") + $dependencies.cmakeArguments
Invoke-Logged $p.cmake $arguments
if (Test-Path (Join-Path $build 'vcpkg_installed')) { throw 'A private dependency installation was created.' }
if ((Get-SharedVcpkgConfiguration $p).statusHash -ne $dependencies.statusHash) { throw 'Shared package records changed.' }
$invalid = $p.Clone()
$invalid.vcpkgInstalled = Join-Path $case 'missing-shared-tree'
$rejected = $false
try { Get-SharedVcpkgConfiguration $invalid } catch {
    if ($_ -notmatch 'Automatic installation is disabled') { throw }
    $rejected = $true
}
if (!$rejected -or (Test-Path $invalid.vcpkgInstalled)) { throw 'Missing dependencies were not rejected without creating a tree.' }
Save-Json (Join-Path $case 'evidence.json') @{dependencies=$dependencies; commands=@($script:CommandRecords.ToArray()); passed=$true}
"Shared-vcpkg checks passed. Evidence: $case"
