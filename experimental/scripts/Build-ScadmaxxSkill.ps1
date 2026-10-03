[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$CustomizerSourceRoot,
    [Parameter(Mandatory)][string]$OutputZip
)
$ErrorActionPreference = 'Stop'
$controlRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$skillRoot = Join-Path $controlRoot 'skills/scadmaxx'
$sourceRoot = (Resolve-Path -LiteralPath $CustomizerSourceRoot).Path
$canonical = Join-Path $sourceRoot 'doc/customizer-attributes.md'
if (!(Test-Path -LiteralPath $canonical -PathType Leaf)) { throw "Missing canonical document: $canonical" }
$destination = [IO.Path]::GetFullPath($OutputZip)
if (Test-Path -LiteralPath $destination) { throw "Output already exists: $destination" }
$sourceRevision = & git -c "safe.directory=$($sourceRoot.Replace('\','/'))" -C $sourceRoot rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot identify source revision' }
$docStatus = & git -c "safe.directory=$($sourceRoot.Replace('\','/'))" -C $sourceRoot status --porcelain -- doc/customizer-attributes.md
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect canonical document status' }
Copy-Item -LiteralPath $canonical -Destination (Join-Path $skillRoot 'references/customizer-attributes.md')
$provenance = [ordered]@{
    canonical_document = 'doc/customizer-attributes.md'
    source_revision = "$sourceRevision".Trim()
    document_modified_from_commit = [bool]$docStatus
    document_sha256 = (Get-FileHash -LiteralPath $canonical -Algorithm SHA256).Hash.ToLowerInvariant()
    note = 'Generated from the canonical source document; refresh with Build-ScadmaxxSkill.ps1. This companion does not assert that every SCADMaxx binary contains these features.'
}
$provenance | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $skillRoot 'references/bundle-source.json') -Encoding utf8
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
Compress-Archive -LiteralPath $skillRoot -DestinationPath $destination
Get-FileHash -LiteralPath $destination -Algorithm SHA256
