#Requires -Version 5.1
<#
.SYNOPSIS
  Przed /noc: git, Postgres, OpenFGA, internet, GitHub.
  Exit 0 = wolno startować zmianę. Exit 1 = stop.
#>
param(
  [switch]$NoStart,
  [switch]$Helper
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $Root "AGENTS.md"))) {
  $Root = (Get-Location).Path
}

if ($Helper) {
  Write-Host "noc-preflight  pas pomocniczy  $((Get-Location).Path)"
  python (Join-Path $Root "scripts\quality\writer_preflight.py") --allow-noc-helper
  if ($LASTEXITCODE -ne 0) {
    Write-Host "noc-preflight: STOP - pas pomocniczy nie na worktree albo noc nie jedzie."
    exit 1
  }
  Write-Host "noc-preflight: OK - pas pomocniczy (bez push na origin/main)."
  exit 0
}

Set-Location $Root

$script:failed = $false

function Write-Ok([string]$Message) {
  Write-Host "OK  $Message"
}

function Write-Fail([string]$Message) {
  Write-Host "FAIL  $Message"
  $script:failed = $true
}

function Test-ListenPort([int]$Port) {
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

Write-Host "noc-preflight  $Root"

python (Join-Path $Root "scripts\quality\writer_preflight.py") --allow-noc
if ($LASTEXITCODE -ne 0) {
  Write-Fail "writer-preflight padł."
}

$dirty = git status --porcelain
if ($dirty) {
  Write-Fail "Drzewo git nieczyste. Inny agent albo niedokończona robota - noc nie startuje."
} else {
  Write-Ok "git czysty"
}

$branch = (git rev-parse --abbrev-ref HEAD).Trim()
if ($branch -ne "main") {
  Write-Fail "Noc jedzie tylko na main (teraz: $branch)."
} else {
  Write-Ok "gałąź main"
}

try {
  $req = [System.Net.HttpWebRequest]::Create("https://github.com")
  $req.Method = "HEAD"
  $req.Timeout = 15000
  $req.AllowAutoRedirect = $true
  $resp = $req.GetResponse()
  $resp.Close()
  Write-Ok "internet (github.com)"
} catch {
  Write-Fail "Brak internetu albo GitHub nie odpowiada: $($_.Exception.Message)"
}

if (-not $script:failed) {
  git fetch origin 2>&1 | Out-Null
  if ($LASTEXITCODE -ne 0) {
    Write-Fail "git fetch origin nie przeszedł (GitHub / remote)."
  } else {
    $null = git ls-remote origin HEAD
    if ($LASTEXITCODE -ne 0) {
      Write-Fail "git ls-remote origin nie przeszedł."
    } else {
      Write-Ok "GitHub git (origin)"
    }
    $local = (git rev-parse HEAD).Trim()
    $remote = (git rev-parse origin/main 2>$null).Trim()
    if (-not $remote) {
      Write-Fail "Brak origin/main po fetch."
    } else {
      $base = (git merge-base HEAD origin/main).Trim()
      if ($local -eq $remote) {
        Write-Ok "main = origin/main"
      } elseif ($base -eq $local) {
        git pull --ff-only origin main
        if ($LASTEXITCODE -ne 0) {
          Write-Fail "origin/main jest do przodu, a pull --ff-only padł."
        } else {
          Write-Ok "dociągnięto origin/main (fast-forward)"
        }
      } elseif ($base -eq $remote) {
        Write-Ok "lokalny main jest do przodu origin (noc wypchnie później)"
      } else {
        Write-Fail "main i origin/main się rozjechały. Noc nie rebase'uje i nie force-pushuje."
      }
    }
  }
}

$pgReady = Test-ListenPort 5432
if (-not $pgReady) {
  $pgIsReady = Get-Command pg_isready -ErrorAction SilentlyContinue
  if ($pgIsReady) {
    & pg_isready -h 127.0.0.1 -p 5432 | Out-Null
    $pgReady = ($LASTEXITCODE -eq 0)
  }
}
if ($pgReady) {
  Write-Ok "Postgres :5432"
} elseif ($NoStart) {
  Write-Fail "Postgres nie nasłuchuje na :5432."
} else {
  $pgCtl = Get-Command pg_ctl -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
  if (-not $pgCtl) {
    $portable = Join-Path $Root "tools\pg16\bin\pg_ctl.exe"
    if (Test-Path $portable) { $pgCtl = $portable }
  }
  $pgData = Join-Path $Root "tools\pgdata"
  if ($pgCtl -and (Test-Path $pgData)) {
    Write-Host "Startuję Postgres (pg_ctl -D tools\\pgdata)…"
    & $pgCtl -D $pgData -o "-p 5432" start | Out-Host
    Start-Sleep -Seconds 2
  }
  if (Test-ListenPort 5432) {
    Write-Ok "Postgres :5432 (uruchomiony)"
  } else {
    Write-Fail "Postgres nie wstaje na :5432. Ręcznie: pg_ctl -D tools\\pgdata -o `"-p 5432`" start"
  }
}

$fgaUp = $false
try {
  $fga = Invoke-WebRequest -Uri "http://127.0.0.1:8080/healthz" -UseBasicParsing -TimeoutSec 3
  if ($fga.StatusCode -ge 200 -and $fga.StatusCode -lt 300) { $fgaUp = $true }
} catch {
  $fgaUp = Test-ListenPort 8080
}
if ($fgaUp) {
  Write-Ok "OpenFGA :8080"
} elseif ($NoStart) {
  Write-Fail "OpenFGA nie odpowiada na :8080/healthz."
} else {
  $fgaExe = Join-Path $Root "tools\openfga\openfga.exe"
  if (Test-Path $fgaExe) {
    Write-Host "Startuję OpenFGA…"
    Start-Process -FilePath $fgaExe -ArgumentList @("run") -WorkingDirectory (Split-Path $fgaExe) -WindowStyle Minimized | Out-Null
    Start-Sleep -Seconds 2
  }
  $fgaUp = $false
  try {
    $fga = Invoke-WebRequest -Uri "http://127.0.0.1:8080/healthz" -UseBasicParsing -TimeoutSec 3
    if ($fga.StatusCode -ge 200 -and $fga.StatusCode -lt 300) { $fgaUp = $true }
  } catch {
    $fgaUp = Test-ListenPort 8080
  }
  if ($fgaUp) {
    Write-Ok "OpenFGA :8080 (uruchomiony)"
  } else {
    Write-Fail "OpenFGA nie wstaje. Ręcznie: tools\\openfga\\openfga.exe run"
  }
}

if ($script:failed) {
  Write-Host "noc-preflight: STOP - nie włączaj pętli /noc."
  exit 1
}
python (Join-Path $Root "scripts\quality\factory_cycle.py") --start noc
if ($LASTEXITCODE -ne 0) {
  Write-Host "noc-preflight: STOP - factory_cycle (retrieve / podłoga jakości)."
  exit 1
}
Write-Host "noc-preflight: OK - wolno /noc."
exit 0
