[CmdletBinding()]
param([string]$Path = (Join-Path $PSScriptRoot 'version.xml'))
$ErrorActionPreference = 'Stop'
# Use an XML parser, with external entities and DTDs disabled.
$settings = New-Object System.Xml.XmlReaderSettings
$settings.DtdProcessing = [System.Xml.DtdProcessing]::Prohibit
$settings.XmlResolver = $null
$reader = [System.Xml.XmlReader]::Create([IO.Path]::GetFullPath($Path), $settings)
try {
    $xml = New-Object System.Xml.XmlDocument
    $xml.XmlResolver = $null
    $xml.Load($reader)
} finally { $reader.Dispose() }
if ($xml.SelectNodes('/version/current').Count -ne 1) { throw 'Expected exactly one version/current element.' }
$parts = foreach ($name in @('major_version', 'minor_version', 'patchlevel')) {
    $nodes = $xml.SelectNodes("/version/current/$name")
    if ($nodes.Count -ne 1 -or $nodes[0].InnerText -cnotmatch '^(0|[1-9][0-9]*)$') {
        throw "Invalid version field: $name"
    }
    $nodes[0].InnerText
}
$nodes = $xml.SelectNodes('/version/current/identifier')
if ($nodes.Count -ne 1) { throw 'Expected exactly one identifier.' }
$identifier = $nodes[0].InnerText
if ($identifier -cnotmatch '^(dev|alpha[1-9][0-9]*|beta[1-9][0-9]*|rc[1-9][0-9]*)?$') {
    throw 'Identifier must be empty, dev, alphaN, betaN, or rcN (N >= 1).'
}
$label = $parts -join '.'
if ($identifier) { $label += "-$identifier" }
$label
