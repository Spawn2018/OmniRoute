#Requires -Version 5.1
<#
.SYNOPSIS
  git push origin main bez zawieszania PowerShell / Cursor na stderr hooka.

.NOTES
  pre-push nadal odpala just gate. Nie używaj 2>&1 | Select-Object na tym pushu —
  NativeCommandError + megabajt coverage historycznie wieszały sesję agenta.
  Exit code = exit code git.
#>
param(
  [string]$Remote = "origin",
  [string]$Branch = "main"
)

$ErrorActionPreference = "Continue"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
  $PSNativeCommandUseErrorActionPreference = $false
}

$Root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $Root "AGENTS.md"))) {
  $Root = (Get-Location).Path
}
Set-Location $Root

$outLog = Join-Path $env:TEMP "omniroute-git-push-out.log"
$errLog = Join-Path $env:TEMP "omniroute-git-push-err.log"
Remove-Item $outLog, $errLog -ErrorAction SilentlyContinue

Write-Host "git-push-main: $Remote $Branch (stdout/stderr -> $env:TEMP\omniroute-git-push-*.log)"

$proc = Start-Process -FilePath "git" `
  -ArgumentList @("push", $Remote, $Branch) `
  -WorkingDirectory $Root `
  -NoNewWindow `
  -Wait `
  -PassThru `
  -RedirectStandardOutput $outLog `
  -RedirectStandardError $errLog

function Write-Tail([string]$Path, [string]$Label, [int]$Lines = 80) {
  if (-not (Test-Path $Path)) {
    return
  }
  $content = Get-Content -LiteralPath $Path -ErrorAction SilentlyContinue
  if (-not $content) {
    return
  }
  Write-Host "--- $Label (ostatnie $Lines) ---"
  $content | Select-Object -Last $Lines | ForEach-Object { Write-Host $_ }
}

Write-Tail $outLog "stdout"
Write-Tail $errLog "stderr"

$code = $proc.ExitCode
if ($null -eq $code) {
  $code = 1
}
if ($code -ne 0) {
  Write-Host "git-push-main: FAIL exit $code (pełne logi: $outLog , $errLog)"
} else {
  Write-Host "git-push-main: OK"
}
exit $code
