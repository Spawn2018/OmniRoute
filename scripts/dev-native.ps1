#Requires -Version 5.1
<#
.SYNOPSIS
  Lokalny stack OmniRoute BEZ Dockera / WSL (Windows natywny).

.DESCRIPTION
  1) Postgres 16 (winget / istniejąca instalacja)
  2) OpenFGA: tools/openfga/openfga.exe (dociągane skryptem)
  3) Migracje Alembic
  4) Opcjonalny seed (org + user + tuple OpenFGA)
  5) Instrukcja startu API + frontend

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts/dev-native.ps1
  powershell -ExecutionPolicy Bypass -File scripts/dev-native.ps1 -SkipInstall -Seed
#>
param(
  [switch]$SkipInstall,
  [switch]$Seed,
  [switch]$DownloadOpenFgaOnly,
  [string]$PgPassword = "omniroute",
  [string]$PgUser = "omniroute",
  [string]$PgDb = "omniroute",
  [string]$OpenFgaVersion = "1.19.0"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $Root "AGENTS.md"))) {
  $Root = Get-Location | Select-Object -ExpandProperty Path
}

function Write-Step([string]$Message) {
  Write-Host ""
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Find-Psql {
  $candidates = @(
    (Get-Command psql -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source),
    "C:\Program Files\PostgreSQL\16\bin\psql.exe",
    "C:\Program Files\PostgreSQL\17\bin\psql.exe",
    "C:\Program Files\PostgreSQL\15\bin\psql.exe"
  ) | Where-Object { $_ -and (Test-Path $_) }
  return $candidates | Select-Object -First 1
}

function Ensure-OpenFga {
  $dir = Join-Path $Root "tools\openfga"
  $exe = Join-Path $dir "openfga.exe"
  if (Test-Path $exe) {
    Write-Host "OpenFGA OK: $exe"
    return $exe
  }
  Write-Step "Pobieram OpenFGA v$OpenFgaVersion (windows_amd64)"
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $url = "https://github.com/openfga/openfga/releases/download/v$OpenFgaVersion/openfga_${OpenFgaVersion}_windows_amd64.tar.gz"
  $tgz = Join-Path $dir "openfga.tgz"
  Invoke-WebRequest -Uri $url -OutFile $tgz -UseBasicParsing
  tar -xzf $tgz -C $dir
  Remove-Item $tgz -Force -ErrorAction SilentlyContinue
  if (-not (Test-Path $exe)) {
    throw "Brak openfga.exe po rozpakowaniu — sprawdź $dir"
  }
  Write-Host "OpenFGA OK: $exe"
  return $exe
}

function Test-Port([int]$Port) {
  try {
    $client = New-Object System.Net.Sockets.TcpClient
    $iar = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
    $ok = $iar.AsyncWaitHandle.WaitOne(800)
    if ($ok -and $client.Connected) {
      $client.Close()
      return $true
    }
    $client.Close()
  } catch {
    return $false
  }
  return $false
}

function Ensure-Postgres {
  $psql = Find-Psql
  if ($psql) {
    Write-Host "psql OK: $psql"
    return $psql
  }
  if ($SkipInstall) {
    throw "Brak psql. Zainstaluj PostgreSQL 16 (winget) albo uruchom bez -SkipInstall."
  }
  Write-Step "Instaluję PostgreSQL 16 przez winget (może wymagać UAC / hasła superusera)"
  Write-Host "Uwaga: instalator EDB pyta o hasło użytkownika 'postgres' — zapamiętaj je."
  winget install --id PostgreSQL.PostgreSQL.16 -e --accept-package-agreements --accept-source-agreements
  $psql = Find-Psql
  if (-not $psql) {
    throw "PostgreSQL zainstalowany, ale psql nie znaleziony. Domknij instalator i dodaj ...\PostgreSQL\16\bin do PATH."
  }
  return $psql
}

function Ensure-Database([string]$PsqlPath) {
  Write-Step "Tworzę rolę/bazę $PgUser / $PgDb (jeśli brak)"
  $env:PGPASSWORD = $PgPassword
  # Próba jako omniroute; jeśli pada — instrukcja dla użytkownika postgres
  $check = & $PsqlPath -h 127.0.0.1 -U $PgUser -d postgres -tAc "SELECT 1" 2>$null
  if ($LASTEXITCODE -ne 0) {
    Write-Host @"

Nie udało się połączyć jako $PgUser@$PgPassword.
Zrób ręcznie (w psql jako użytkownik postgres):

  CREATE USER $PgUser WITH PASSWORD '$PgPassword' CREATEDB;
  CREATE DATABASE $PgDb OWNER $PgUser;
  CREATE DATABASE omniroute_test OWNER $PgUser;
  CREATE ROLE tenant_tester LOGIN PASSWORD 'test' NOINHERIT NOBYPASSRLS;
  GRANT ALL ON DATABASE $PgDb TO $PgUser;
  GRANT ALL ON DATABASE omniroute_test TO $PgUser;

Potem: .\scripts\dev-native.ps1 -SkipInstall -Seed

"@ -ForegroundColor Yellow
    return $false
  }

  & $PsqlPath -h 127.0.0.1 -U $PgUser -d postgres -v ON_ERROR_STOP=1 -c "SELECT 1" | Out-Null
  $exists = & $PsqlPath -h 127.0.0.1 -U $PgUser -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$PgDb'"
  if ($exists.Trim() -ne "1") {
    & $PsqlPath -h 127.0.0.1 -U $PgUser -d postgres -c "CREATE DATABASE $PgDb OWNER $PgUser"
  }
  $existsTest = & $PsqlPath -h 127.0.0.1 -U $PgUser -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='omniroute_test'"
  if ($existsTest.Trim() -ne "1") {
    & $PsqlPath -h 127.0.0.1 -U $PgUser -d postgres -c "CREATE DATABASE omniroute_test OWNER $PgUser"
  }
  Write-Host "Bazy OK ($PgDb, omniroute_test)"
  return $true
}

function Ensure-EnvFile {
  $envFile = Join-Path $Root ".env"
  if (Test-Path $envFile) {
    Write-Host ".env już istnieje — nie nadpisuję"
    return
  }
  Write-Step "Tworzę .env z .env.example"
  Copy-Item (Join-Path $Root ".env.example") $envFile
}

function Run-Migrations {
  Write-Step "Alembic upgrade head"
  Push-Location (Join-Path $Root "backend")
  try {
    $env:DATABASE_URL_SYNC = "postgresql://${PgUser}:${PgPassword}@127.0.0.1:5432/${PgDb}"
    $env:DATABASE_URL = "postgresql+asyncpg://${PgUser}:${PgPassword}@127.0.0.1:5432/${PgDb}"
    python -m alembic upgrade head
  } finally {
    Pop-Location
  }
}

function Start-OpenFgaProcess([string]$Exe) {
  if (Test-Port 8080) {
    Write-Host "Port 8080 już zajęty — zakładam działające OpenFGA"
    return $null
  }
  Write-Step "Start OpenFGA (in-memory) na :8080"
  $proc = Start-Process -FilePath $Exe -ArgumentList @("run") -WorkingDirectory (Split-Path $Exe) -PassThru -WindowStyle Minimized
  Start-Sleep -Seconds 2
  if (-not (Test-Port 8080)) {
    throw "OpenFGA nie nasłuchuje na :8080 (pid=$($proc.Id))"
  }
  Write-Host "OpenFGA PID $($proc.Id)"
  return $proc
}

# --- main ---
Set-Location $Root
Write-Host "OmniRoute native dev — $Root"

$openfgaExe = Ensure-OpenFga
if ($DownloadOpenFgaOnly) {
  Write-Host "Gotowe (tylko OpenFGA)."
  exit 0
}

$psql = Ensure-Postgres
$dbOk = Ensure-Database $psql
Ensure-EnvFile

if ($dbOk) {
  Run-Migrations
} else {
  Write-Host "Pomijam migracje — najpierw skonfiguruj bazę." -ForegroundColor Yellow
}

$fgaProc = Start-OpenFgaProcess $openfgaExe

if ($Seed -and $dbOk) {
  Write-Step "Seed lokalny (org/user + OpenFGA)"
  python (Join-Path $Root "scripts\dev_seed_local.py")
}

Write-Host @"

----------------------------------------------------------
NASTĘPNE KROKI (dwa terminale PowerShell):

1) API:
   cd $Root\backend
   `$env:DATABASE_URL='postgresql+asyncpg://${PgUser}:${PgPassword}@127.0.0.1:5432/${PgDb}'
   `$env:DATABASE_URL_SYNC='postgresql://${PgUser}:${PgPassword}@127.0.0.1:5432/${PgDb}'
   `$env:OPENFGA_API_URL='http://127.0.0.1:8080'
   # po seedzie ustaw OPENFGA_STORE_ID / OPENFGA_MODEL_ID z outputu
   python -m granian --interface asgi app.main:app --reload --host 127.0.0.1 --port 8000

2) Frontend:
   cd $Root\frontend
   pnpm dev

Sesja w UI: wklej organization_id + user_id ze seeda.
Testy RLS (gdy Postgres działa):
   `$env:ADMIN_TEST_DATABASE_URL='postgresql+asyncpg://${PgUser}:${PgPassword}@127.0.0.1:5432/omniroute_test'
   `$env:TENANT_TEST_DATABASE_URL='postgresql+asyncpg://tenant_tester:test@127.0.0.1:5432/omniroute_test'
   python -m pytest backend/tests -m integration -q

OpenFGA binary: $openfgaExe
----------------------------------------------------------
"@ -ForegroundColor Green
