#Requires -Version 5.1
<#
.SYNOPSIS
  Włącza wersjonowane hooki gita (scripts/githooks) w tym klonie repozytorium.

.DESCRIPTION
  Katalog .git/hooks nie da się wersjonować, więc hooki leżą w scripts/githooks,
  a git dostaje wskazanie przez core.hooksPath. Ustawienie jest lokalne dla klonu
  i trzeba je powtórzyć po każdym świeżym clone.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/install-hooks.ps1
#>
$ErrorActionPreference = "Stop"
# Konsola Windows startuje na cp852 i zjada polskie znaki z komunikatów poniżej.
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path (Join-Path $root "scripts/githooks/pre-push"))) {
    throw "Brak scripts/githooks/pre-push — uruchamiasz skrypt spoza repozytorium OmniRoute?"
}

git config core.hooksPath scripts/githooks

$configured = git config --get core.hooksPath
if ($configured -ne "scripts/githooks") {
    throw "core.hooksPath = '$configured' zamiast 'scripts/githooks' — instalacja nieudana."
}

Write-Host "core.hooksPath = $configured"
Write-Host "pre-push odpala 'just gate' (ok. 70 s) i blokuje push, gdy bramka pada."
Write-Host "Furtka awaryjna, tylko wyjątkowo: git push --no-verify"
