# Tool Guardian — PreToolUse hook (Windows)
param()

if ($env:SKIP_TOOL_GUARD -eq "true") { exit 0 }

$GuardMode = if ($env:GUARD_MODE) { $env:GUARD_MODE } else { "block" }
$LogDir = if ($env:TOOL_GUARD_LOG_DIR) { $env:TOOL_GUARD_LOG_DIR } else { "logs\copilot\tool-guardian" }

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$input_json = $input | Out-String
$scanText = $input_json

if ($scanText -match "rm\s+-r\s*f?\s*/|git\s+push\s+--force|DROP\s+DATABASE|curl\s+.*\|\s*bash") {
    $logEntry = @{ timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"); event = "threats_detected"; mode = $GuardMode } | ConvertTo-Json -Compress
    Add-Content -Path "$LogDir\guard.log" -Value $logEntry

    if ($GuardMode -eq "block") {
        @{ hookSpecificOutput = @{ hookEventName = "PreToolUse"; permissionDecision = "deny"; permissionDecisionReason = "Tool Guardian: potentially destructive command detected" } } | ConvertTo-Json -Compress
        exit 2
    }
}

$okLog = @{ timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"); event = "guard_passed"; mode = $GuardMode } | ConvertTo-Json -Compress
Add-Content -Path "$LogDir\guard.log" -Value $okLog
exit 0
