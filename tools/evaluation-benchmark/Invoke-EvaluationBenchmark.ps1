#requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Executable,
    [Parameter(Mandatory)][string]$SourceDirectory,
    [Parameter(Mandatory)][string]$OutputDirectory,
    [ValidateSet('panel', 'brackets-core', 'brackets-hull', 'brackets-minkowski', 'brackets-full')]
    [string[]]$Workload = @('panel', 'brackets-core', 'brackets-hull', 'brackets-minkowski', 'brackets-full'),
    [ValidateSet('baseline', 'local', 'global')][string[]]$Scenario = @('baseline', 'local', 'global'),
    [ValidateSet('csg', 'off', 'stl', 'preview')][string[]]$Stage = @('csg', 'off'),
    [ValidateRange(0, 2)][int]$Quality = 1,
    [ValidateRange(1, 10)][int]$Repetitions = 3,
    [switch]$AnimationSequence,
    [ValidateRange(1, 600)][int]$TimeoutSeconds = 45
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Executable = (Resolve-Path -LiteralPath $Executable).Path
$SourceDirectory = (Resolve-Path -LiteralPath $SourceDirectory).Path
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $OutputDirectory) { throw "Use a new output directory: $OutputDirectory" }
$fixtures = Join-Path $SourceDirectory 'tests/data/scad/benchmarks/edit-evaluation'
$catalogPath = Join-Path $PSScriptRoot 'cases.json'
$catalog = Get-Content -LiteralPath $catalogPath -Raw | ConvertFrom-Json
$cases = @($catalog.workloads | Where-Object name -In $Workload)
foreach ($case in $cases) {
    if (!(Test-Path -LiteralPath (Join-Path $fixtures $case.file))) { throw "Missing fixture: $($case.file)" }
}
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null

function Invoke-Tool([string[]]$Arguments, [string]$LogStem) {
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $Executable
    $start.WorkingDirectory = $OutputDirectory
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    foreach ($arg in $Arguments) { $start.ArgumentList.Add($arg) }
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $process.Start() | Out-Null
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $timedOut = !$process.WaitForExit($TimeoutSeconds * 1000)
    if ($timedOut) { $process.Kill($true); $process.WaitForExit() }
    $timer.Stop()
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    [IO.File]::WriteAllText("$LogStem.stdout.txt", $stdout)
    [IO.File]::WriteAllText("$LogStem.stderr.txt", $stderr)
    $result = [ordered]@{
        seconds = $timer.Elapsed.TotalSeconds
        exitCode = $process.ExitCode
        timedOut = $timedOut
        diagnosticsFailed = ($stderr + $stdout) -match '(?im)^\s*(WARNING:|ERROR:|Parser error:)|Current top level object is empty'
        arguments = $Arguments
    }
    $process.Dispose()
    return $result
}

$version = Invoke-Tool @('--version') (Join-Path $OutputDirectory 'version')
if ($version.exitCode -ne 0 -or $version.timedOut) { throw 'Executable version probe failed' }
$head = (& git -C $SourceDirectory rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Source identity failed' }
$metadata = [ordered]@{
    schemaVersion = 1
    utc = [DateTime]::UtcNow.ToString('o')
    executable = $Executable
    executableSha256 = (Get-FileHash -LiteralPath $Executable).Hash
    guiExecutableSha256 = $null
    sourceDirectory = $SourceDirectory
    sourceHead = $head
    sourceStatus = @(& git -C $SourceDirectory status --short)
    timingScope = 'Fresh process wall time, including startup and output serialization; OS caches may be warm. NOT persistent-session edit latency.'
    animationSequence = [bool]$AnimationSequence
    binaryMatchesSource = 'Not inferred. Consult executable-build-info.json and sourceHead separately.'
    backend = 'Manifold'
    quality = $Quality
    repetitions = $Repetitions
    timeoutSeconds = $TimeoutSeconds
    processor = (Get-CimInstance Win32_Processor | Select-Object -First 1 Name, NumberOfCores, NumberOfLogicalProcessors)
    os = [Environment]::OSVersion.VersionString
    powershell = $PSVersionTable.PSVersion.ToString()
    runnerSha256 = (Get-FileHash -LiteralPath $PSCommandPath).Hash
    catalogSha256 = (Get-FileHash -LiteralPath $catalogPath).Hash
    fixtureHashes = @($cases.file | Sort-Object -Unique | ForEach-Object {
        @{ file = $_; sha256 = (Get-FileHash -LiteralPath (Join-Path $fixtures $_)).Hash }
    })
}
if ($AnimationSequence) {
    $metadata.timingScope = 'Six frames in one process: base,A,A,B,B,base; caches persist and AST is parsed once. Batch wall time includes instantiation and exports. Frame geometry summaries exclude SCAD execution. NOT GUI edit latency.'
}
$guiExecutable = [IO.Path]::ChangeExtension($Executable, '.exe')
if (Test-Path -LiteralPath $guiExecutable) { $metadata.guiExecutableSha256 = (Get-FileHash -LiteralPath $guiExecutable).Hash }
$buildInfo = Join-Path (Split-Path $Executable) 'build-info.json'
if (Test-Path -LiteralPath $buildInfo) { Copy-Item -LiteralPath $buildInfo -Destination (Join-Path $OutputDirectory 'executable-build-info.json') }
$metadata | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'metadata.json')
$records = [Collections.Generic.List[object]]::new()

# Rotate workload ordering between repetitions; run sequentially to avoid self-contention.
for ($repeat = 0; $repeat -lt $Repetitions; $repeat++) {
    for ($offset = 0; $offset -lt $cases.Count; $offset++) {
        $case = $cases[($offset + $repeat) % $cases.Count]
        foreach ($scenarioName in $Scenario) {
            foreach ($stageName in $Stage) {
                $id = '{0}-{1}-{2}-r{3}' -f $case.name, $scenarioName, $stageName, ($repeat + 1)
                $stem = Join-Path $OutputDirectory $id
                $extension = if ($stageName -eq 'preview') { 'png' } else { $stageName }
                $output = "$stem.$extension"
                $arguments = @('--backend=Manifold', '--hardwarnings', '-o', $output, '-D', "quality=$Quality")
                foreach ($define in $case.defines) { $arguments += @('-D', $define) }
                if ($AnimationSequence) {
                    $arguments += '--animate=6'
                    if ($scenarioName -ne 'baseline') {
                        $assignment = if ($scenarioName -eq 'local') { $case.localEdit } else { $case.globalEdit }
                        $parts = $assignment.Split('=', 2)
                        $initial = if ($scenarioName -eq 'local') { '0' } else {
                            ([double]$case.globalBase).ToString([Globalization.CultureInfo]::InvariantCulture)
                        }
                        # Keep arithmetic in SCAD, preserving culture-independent decimal literals.
                        $define = '{0}=[{1},{2},{2},{1}+1.25*({2}-{1}),{1}+1.25*({2}-{1}),{1}][min(5,floor($t*6+0.1))]' -f $parts[0], $initial, $parts[1]
                        $arguments += @('-D', $define)
                    }
                } else {
                    if ($scenarioName -eq 'local') { $arguments += @('-D', $case.localEdit) }
                    if ($scenarioName -eq 'global') { $arguments += @('-D', $case.globalEdit) }
                }
                if ($stageName -in @('stl', 'off')) {
                    $summaryTarget = if ($AnimationSequence) { '-' } else { "$stem.summary.json" }
                    $arguments += @('--summary=all', '--summary-file', $summaryTarget)
                    if ($stageName -eq 'stl') { $arguments += '--export-format=binstl' }
                } elseif ($stageName -eq 'preview') {
                    $arguments += @('--imgsize=1000,700', '--viewall', '--autocenter', '--projection=o')
                }
                $arguments += (Join-Path $fixtures $case.file)
                $result = Invoke-Tool $arguments $stem
                $outputs = if ($AnimationSequence) { @(0..5 | ForEach-Object { '{0}{1:D5}.{2}' -f $stem, $_, $extension }) } else { @($output) }
                $outputRecords = @($outputs | ForEach-Object {
                    $exists = Test-Path -LiteralPath $_
                    [pscustomobject]@{
                        path = $_
                        bytes = $(if ($exists) { (Get-Item -LiteralPath $_).Length } else { 0 })
                        sha256 = $(if ($exists) { (Get-FileHash -LiteralPath $_).Hash } else { $null })
                    }
                })
                $frameSummaries = @()
                if ($AnimationSequence -and $stageName -in @('stl', 'off')) {
                    # OpenSCAD does not terminate stdout summary JSON with a newline;
                    # the next frame's "Exporting ..." status can follow its closing brace.
                    $frameSummaries = @(Get-Content -LiteralPath "$stem.stdout.txt" | Where-Object { $_.StartsWith('{') } | ForEach-Object {
                        $_.Substring(0, $_.LastIndexOf('}') + 1) | ConvertFrom-Json
                    })
                }
                $bytes = ($outputRecords | Measure-Object -Property bytes -Sum).Sum
                $passed = !$result.timedOut -and $result.exitCode -eq 0 -and !$result.diagnosticsFailed -and @($outputRecords | Where-Object bytes -LE 0).Count -eq 0
                if ($AnimationSequence -and $stageName -in @('stl', 'off') -and $frameSummaries.Count -ne 6) { $passed = $false }
                if ($passed -and $stageName -eq 'csg') {
                    foreach ($compiled in $outputs) {
                        $text = Get-Content -LiteralPath $compiled -Raw
                        foreach ($operator in @('hull', 'minkowski')) {
                            $present = $text -match "\b$operator\s*\("
                            if ($present -ne ($operator -in $case.advancedOperators)) { $passed = $false }
                        }
                    }
                }
                $record = [ordered]@{
                    id = $id; workload = $case.name; scenario = $scenarioName; stage = $stageName
                    repetition = $repeat + 1; seconds = $result.seconds; passed = $passed
                    exitCode = $result.exitCode; timedOut = $result.timedOut
                    diagnosticsFailed = $result.diagnosticsFailed
                    bytes = $bytes; outputs = $outputRecords; frameSummaries = $frameSummaries
                    arguments = $result.arguments
                }
                $records.Add([pscustomobject]$record)
                $records | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'results.json')
                Write-Host ('{0}: {1:N3}s, passed={2}' -f $id, $result.seconds, $passed)
                if (!$passed) { throw "Benchmark failed: $id; inspect $stem.stderr.txt. Partial evidence retained." }
            }
        }
    }
}
$summary = foreach ($group in ($records | Group-Object workload, scenario, stage)) {
    $times = @($group.Group.seconds | Sort-Object)
    $mid = [int][Math]::Floor($times.Count / 2)
    $median = if ($times.Count % 2) { $times[$mid] } else { ($times[$mid-1] + $times[$mid]) / 2 }
    [pscustomobject]@{
        workload = $group.Group[0].workload; scenario = $group.Group[0].scenario; stage = $group.Group[0].stage
        samples = $times.Count; medianSeconds = $median; minSeconds = $times[0]; maxSeconds = $times[-1]
    }
}
$summary | Export-Csv -LiteralPath (Join-Path $OutputDirectory 'summary.csv') -NoTypeInformation
$summary | Format-Table -AutoSize
