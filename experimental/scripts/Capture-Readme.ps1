#requires -Version 7.2
[CmdletBinding()]
param(
    [ValidateSet('Configure','Build','Capture')][string]$Step = 'Capture',
    [string]$Source = 'D:/openscad/wt-openscad-readme-captures',
    [string]$Build = 'D:/openscad/runs/readme-captures/build',
    [string]$Output = ('D:/openscad/runs/readme-captures/' + (Get-Date -Format yyyyMMddTHHmmss)),
    [string]$BuildProfile = (Join-Path $PSScriptRoot '../profiles/this-machine.local.json'),
    [string]$Model = (Join-Path $PSScriptRoot '../../docs/screenshots/models/mounting-bracket.scad'),
    [string]$Recipe = (Join-Path $PSScriptRoot '../readme-captures.json')
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath (Join-Path $Source 'CMakeLists.txt') -PathType Leaf)) {
    throw "Capture source checkout is missing: $Source. Recreate it from its retained branch or pass -Source; see docs/readme-capture-tool.md."
}
$profile = Get-Content -LiteralPath $BuildProfile -Raw | ConvertFrom-Json
$triplet = "$($profile.vcpkgInstalled)/x64-windows"
Import-Module (Join-Path $profile.visualStudio 'Common7/Tools/Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $profile.visualStudio -Arch amd64 -HostArch amd64 -SkipAutomaticLocation `
    -DevCmdArguments "-vcvars_ver=$($profile.toolset) -winsdk=$($profile.sdk)" | Out-Null
$env:PATH = ("C:/Program Files/Git/usr/bin;C:/Program Files/Git/mingw64/bin;$triplet/tools/gettext/bin;$triplet/bin".Replace('/','\')) + ";$env:PATH"
New-Item -ItemType Directory -Force -Path $Build | Out-Null
$log = Join-Path $Build ((Get-Date -Format yyyyMMddTHHmmss) + "-$Step.log")
if ($Step -eq 'Configure') {
    $ninja = Join-Path $profile.visualStudio 'Common7/IDE/CommonExtensions/Microsoft/CMake/Ninja/ninja.exe'
    $compiler = Join-Path $env:VCToolsInstallDir 'bin/Hostx64/x64/cl.exe'
    & $profile.cmake -S $Source -B $Build -G Ninja "-DCMAKE_MAKE_PROGRAM=$ninja" `
        '-DCMAKE_BUILD_TYPE=Release' "-DCMAKE_C_COMPILER=$compiler" "-DCMAKE_CXX_COMPILER=$compiler" `
        "-DCMAKE_TOOLCHAIN_FILE=$($profile.vcpkg)/scripts/buildsystems/vcpkg.cmake" `
        "-DVCPKG_INSTALLED_DIR=$($profile.vcpkgInstalled)" -DVCPKG_MANIFEST_MODE=OFF -DVCPKG_MANIFEST_INSTALL=OFF `
        -DHEADLESS=OFF -DUSE_QT6=ON -DUSE_BUILTIN_OPENCSG=ON -DENABLE_TESTS=OFF -DENABLE_GUI_TESTS=ON `
        -DENABLE_NAVIGATION_CUBE_TUNING=ON "-DFLEX_EXECUTABLE=$($profile.flex)" "-DBISON_EXECUTABLE=$($profile.bison)" `
        "-DQT6QSCINTILLA_INCLUDE_DIR=$triplet/include/Qt6/Qsci" "-DQT6QSCINTILLA_LIBRARY=$triplet/lib/qscintilla2_qt6.lib" `
        2>&1 | Tee-Object $log
    if ($LASTEXITCODE) { throw "Configure failed; see $log" }
} elseif ($Step -eq 'Build') {
    & $profile.cmake --build $Build --target OpenSCADExe --parallel 4 2>&1 | Tee-Object $log
    if ($LASTEXITCODE) { throw "Build failed; see $log" }
} else {
    if (Test-Path -LiteralPath $Output) { throw 'Choose a fresh output directory; existing captures are preserved.' }
    New-Item -ItemType Directory -Path $Output | Out-Null
    $Output = (Resolve-Path -LiteralPath $Output).Path
    $env:QT_PLUGIN_PATH = "$triplet/Qt6/plugins"
    $env:QT_QPA_PLATFORM = 'windows'
    $env:QT_SCALE_FACTOR = '1'
    $env:OPENSCAD_TEST_SETTINGS_DIR = Join-Path $Output 'settings'
    $env:OPENSCAD_README_OUTPUT = $Output
    $env:OPENSCAD_README_RECIPE = (Resolve-Path -LiteralPath $Recipe).Path
    foreach ($resource in @('shaders','color-schemes','fonts','locale')) {
        Copy-Item -LiteralPath (Join-Path $Source $resource) -Destination $Build -Recurse -Force
    }
    Copy-Item -LiteralPath $Model -Destination "$Output/mounting-bracket.scad"
    Copy-Item -LiteralPath $Recipe -Destination "$Output/recipe.json"
    $process = Start-Process -FilePath "$Build/openscad.exe" -ArgumentList @('--run-all-gui-tests',
        ('"' + "$Output/mounting-bracket.scad" + '"')) -WorkingDirectory $Output -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput "$Output/stdout.log" -RedirectStandardError "$Output/stderr.log"
    if (!$process.WaitForExit(60000)) { throw "Capture still running as PID $($process.Id); inspect before retrying." }
    if ($process.ExitCode -ne 0) { throw "Capture failed: $($process.ExitCode). See $Output/stderr.log" }
    if (!(Test-Path "$Output/captures.json")) { throw 'Capture hook did not produce its manifest.' }
    $gitSource = $Source.Replace('\','/')
    & git -c "safe.directory=$gitSource" -C $Source diff --binary | Set-Content "$Output/source-changes.patch"
    $hooks = @(Get-Item "$Source/src/guitests/guitests.cc")
    if (Test-Path "$Source/src/guitests/ReadmeCapture.cc") { $hooks += Get-Item "$Source/src/guitests/ReadmeCapture.cc" }
    foreach ($hook in $hooks) { Copy-Item -LiteralPath $hook.FullName -Destination (Join-Path $Output $hook.Name) }
    @{source=$Source; head=(& git -c "safe.directory=$gitSource" -C $Source rev-parse HEAD);
        dirty=(& git -c "safe.directory=$gitSource" -C $Source status --porcelain);
        hookSha256=@($hooks | Get-FileHash | Select-Object Path,Hash);
        binarySha256=(Get-FileHash "$Build/openscad.exe").Hash; modelSha256=(Get-FileHash $Model).Hash;
        recipeSha256=(Get-FileHash $Recipe).Hash; scale=1} |
        ConvertTo-Json -Depth 4 | Set-Content "$Output/provenance.json"
    Write-Output "Captures: $Output"
}
