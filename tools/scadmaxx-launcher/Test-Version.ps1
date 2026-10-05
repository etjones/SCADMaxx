$ErrorActionPreference = 'Stop'
$readVersion = Join-Path $PSScriptRoot 'Get-Version.ps1'
$temp = Join-Path ([IO.Path]::GetTempPath()) ('launcher-version-test-' + [guid]::NewGuid())
New-Item -ItemType Directory $temp | Out-Null
$path = Join-Path $temp 'version.xml'
try {
    foreach ($case in @(
        @('0', '1', '0', '', '0.1.0'),
        @('2', '3', '4', 'rc2', '2.3.4-rc2'),
        @('0', '1', '0', 'dev', '0.1.0-dev'),
        @('01', '1', '0', '', ''),
        @('0', '-1', '0', '', ''),
        @('0', '1', '0', '../bad', '')
    )) {
        $content = '<version><current><major_version>{0}</major_version><minor_version>{1}</minor_version><patchlevel>{2}</patchlevel><identifier>{3}</identifier></current></version>' -f $case[0], $case[1], $case[2], $case[3]
        Set-Content $path $content -Encoding UTF8
        $before = (Get-FileHash $path).Hash
        $failed = $false
        try { $actual = & $readVersion -Path $path } catch { $failed = $true }
        if ($case[4]) {
            if ($failed -or $actual -cne $case[4]) { throw "Wrong version for $content" }
        } elseif (!$failed) { throw "Accepted invalid version: $content" }
        if ((Get-FileHash $path).Hash -ne $before) { throw 'Reader modified XML.' }
    }
    foreach ($content in @('<version/>', '<version>', '<!DOCTYPE version [<!ENTITY x "0">]><version/>')) {
        Set-Content $path $content -Encoding UTF8
        $failed = $false
        try { & $readVersion -Path $path | Out-Null } catch { $failed = $true }
        if (!$failed) { throw "Accepted malformed or unsupported XML: $content" }
    }
    Write-Host 'Version parsing, validation and read-only checks passed.'
} finally {
    Remove-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $temp -Force
}
