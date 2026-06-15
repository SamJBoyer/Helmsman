#Requires -Version 5.1
<#
.SYNOPSIS
  Bootstrap Windows host for Helmsman (Docker Desktop, VcXsrv).

.DESCRIPTION
  Installs native AMD64 tooling via WinGet.
  Run from the Helmsman repo root. Docker Desktop enables the WSL2
  backend on its own — no separate WSL distro install.

.EXAMPLE
  .\scripts\bootstrap.ps1

.EXAMPLE
  .\scripts\bootstrap.ps1 -SkipWinget
#>
[CmdletBinding()]
param(
    [switch]$SkipWinget
)

$ErrorActionPreference = 'Stop'

# WinGet package IDs (AMD64 / native targets via winget source)
$WingetPackages = @(
    @{ Id = 'Docker.DockerDesktop'; Name = 'Docker Desktop' },
    @{ Id = 'marha.VcXsrv';        Name = 'VcXsrv' }
)

function Write-Step([string]$Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Invoke-WingetInstall([string]$Id, [string]$DisplayName) {
    $list = winget list --id $Id --accept-source-agreements 2>$null
    if ($LASTEXITCODE -eq 0 -and $list -match [regex]::Escape($Id)) {
        Write-Host "  [skip] $DisplayName already installed ($Id)" -ForegroundColor DarkGray
        return
    }

    Write-Host "  [install] $DisplayName ($Id)..." -ForegroundColor Yellow
    winget install `
        --id $Id `
        --exact `
        --source winget `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity

    if ($LASTEXITCODE -ne 0) {
        throw "winget install failed for $Id (exit $LASTEXITCODE)"
    }
    Write-Host "  [ok] $DisplayName" -ForegroundColor Green
}

# --- Main ---

Write-Host 'Helmsman — Windows host bootstrap' -ForegroundColor Cyan

if (-not (Get-Command winget -ErrorAction SilentlyContinue) -and -not $SkipWinget) {
    throw 'winget is not available. Install "App Installer" from the Microsoft Store, then re-run.'
}

if (-not $SkipWinget) {
    Write-Step 'WinGet packages (native AMD64)'
    foreach ($pkg in $WingetPackages) {
        Invoke-WingetInstall -Id $pkg.Id -DisplayName $pkg.Name
    }
}

Write-Step 'Post-install reminders'
Write-Host @"
  1. Open Docker Desktop -> Settings -> General -> enable "Use the WSL 2 based engine".
  2. Start VcXsrv (XLaunch): disable native OpenGL; allow connections from Docker subnets. DISPLAY=host.docker.internal:0.0.
  3. Set user env GITHUB_USER (lowercase) for GHCR/devcontainer, e.g. samjboyer.
  4. Build dev image: .\modules\devcontainer\scripts\build-image.ps1
"@ -ForegroundColor DarkGray

Write-Host "`nHost bootstrap finished." -ForegroundColor Green
