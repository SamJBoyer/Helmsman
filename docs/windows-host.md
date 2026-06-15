# Windows host configuration

Checklist for the bare-metal tier (Unity, Quest, GPU, Docker) when running Helmsman.

For manual steps scripts cannot automate (Git auth, Cursor attach, Unity UI, etc.), see [modules/devcontainer/docs/manual-and-limits.md](../modules/devcontainer/docs/manual-and-limits.md).

## Automated install (recommended)

Run from the Helmsman repo root:

```powershell
cd C:\Users\samja\Desktop\Helmsman
.\scripts\bootstrap.ps1
```

This script:

| Layer | Action |
|-------|--------|
| Docker Desktop | `winget install Docker.DockerDesktop --exact --source winget` |
| VcXsrv | `winget install marha.VcXsrv --exact --source winget` |

Docker Desktop enables the WSL2 backend internally (`docker-desktop` distros). No separate WSL Ubuntu install is required.

## BIOS / virtualization

- [ ] Enable **Intel VT-x** in UEFI/BIOS.
- [ ] Optional: **VT-d** if you plan device passthrough later.

Verify in PowerShell:

```powershell
(Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled
systeminfo | Select-String -Pattern "Hyper-V"
```

Expected: virtualization enabled; hypervisor detected when Docker Desktop is installed.

## Docker Desktop

- [ ] Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) (**AMD64**).
- [ ] **Settings → General → Use the WSL 2 based engine** — enabled (Docker manages WSL2 internally; no host WSL distro needed).
- [ ] **Settings → Resources**: allocate enough RAM/CPU for C++/vcpkg builds (e.g. 8+ GB RAM).

## X11 display (GUI from container)

Helmsman uses **X11 over the network**, not WSLg. Run an X server on Windows (e.g. [VcXsrv](https://sourceforge.net/projects/vcxsrv/)) before using GUI tools inside the devcontainer.

- [ ] VcXsrv: disable native OpenGL; allow connections from Docker virtual subnets.
- [ ] Container `DISPLAY` defaults to `host.docker.internal:0.0` (see `modules/devcontainer/docker/container-bashrc.sh`).
- [ ] Override in `.devcontainer/.env` if your X server uses a different port.

Verify:

```powershell
docker version
docker run --rm hello-world
```

## Environment variable for devcontainers

Set a **User** environment variable (System Properties → Environment Variables):

| Variable       | Example              |
|----------------|----------------------|
| `GITHUB_USER`  | your-github-username |

Restart Cursor after changing.

## Meta Quest USB (`usbipd-win`)

**Default:** Quest development on **Windows** (Unity, Meta XR SDK, `hzdb`). Do not rely on USB inside the Linux devcontainer.

When a **WSL/Linux** tool needs the device (e.g. `adb`):

```powershell
winget install dorssel.usbipd-win
usbipd list
usbipd bind --busid <BUSID>
usbipd attach --wsl --busid <BUSID>
```

Re-run `attach` after unplugging the cable.

## Build the portable image

```powershell
cd C:\Users\samja\Desktop\Helmsman
$env:GITHUB_USER = "your-github-username"
.\modules\devcontainer\scripts\build-image.ps1
```

See [modules/devcontainer/docs/ghcr.md](../modules/devcontainer/docs/ghcr.md) for push/login.

## Pin Miniconda installer (optional)

To lock the Miniconda installer hash in CI:

```powershell
curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
(Get-FileHash miniconda.sh -Algorithm SHA256).Hash.ToLower()
```

Pass at build time:

```dockerfile
# docker build --build-arg MINICONDA_SHA256=<hash> ...
```

Or set `MINICONDA_SHA256` in `modules/devcontainer/docker/install-miniconda.sh` when maintaining a pinned pipeline.
