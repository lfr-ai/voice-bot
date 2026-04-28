# Check Licenses — Stop hook (Windows)
param()

if ($env:SKIP_LICENSE_CHECK -eq "true") { exit 0 }

$Mode = if ($env:LICENSE_MODE) { $env:LICENSE_MODE } else { "warn" }
$LogDir = if ($env:LICENSE_LOG_DIR) { $env:LICENSE_LOG_DIR } else { "logs\copilot\license-checker" }

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

if (Get-Command pip-licenses -ErrorAction SilentlyContinue) {
    try {
        pip-licenses --format=json | Out-Null
        $entry = @{ timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"); event = "license_check_ok"; mode = $Mode } | ConvertTo-Json -Compress
        Add-Content -Path "$LogDir\license.log" -Value $entry
        exit 0
    }
    catch {
        Write-Host "[License Check] pip-licenses failed; continuing in $Mode mode." -ForegroundColor Yellow
    }
}

if ($Mode -eq "block") { exit 1 }
exit 0
