param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = "Stop"
$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$configPath = Join-Path $resolvedRoot "config\hermes.json"
if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) { throw "ERR_HERMES_CONFIG_MISSING" }
$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
$hermes = [string]$config.executable
if (-not (Test-Path -LiteralPath $hermes -PathType Leaf)) { throw "ERR_HERMES_EXECUTABLE_MISSING" }

$output = & $hermes --version 2>&1
if ($LASTEXITCODE -ne 0) { throw "ERR_HERMES_VERSION_COMMAND" }
$expected = "Hermes Agent v$($config.release.version) ($($config.release.tag.Substring(1)))"
if (($output -join "`n") -notmatch [regex]::Escape($expected)) { throw "ERR_HERMES_VERSION_MISMATCH" }
$output
exit 0
