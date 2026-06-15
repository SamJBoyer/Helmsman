To bring Helmsman to life under this Manifest Conductor architecture, your implementation roadmap falls into three distinct phases.

Here is your concrete list of action items, organized by where the code will actually be written.

Phase 1: Build the Helmsman Repo (The Host-Side Orchestrator)
This code runs natively on the Windows host and acts as the gatekeeper and bootstrap engine.

[ ] Create the Master Repository Structure:

Set up a clean root directory (/helmsman).

Initialize the core repositories as tracked Git submodules or write an optimization script to auto-clone them into designated sub-directories:

/modules/devcontainer

/modules/mcp-server

/modules/harness-builder

/modules/skills-repo

[x] Develop the host bootstrap script (`bootstrap.ps1`):

`scripts/bootstrap.ps1` — installs Docker Desktop and VcXsrv via WinGet. See `docs/windows-host.md`.

[ ] Build the Secret Injector:

Create a .env.template file containing keys for your LLM providers and GitHub access.

Write an interactive TUI or CLI script (helmsman setup) that prompts for missing keys on a first-run setup, aggregates them, and writes a local, untracked master .env file directly to the host filesystem.

[ ] Write the Master Ignition Script (helmsman launch):

Create the primary entry script that reads the configuration maps and triggers the IDE CLI command to spin up the Dev Container workspace (cursor ./modules/devcontainer).

Phase 2: Configure the Dev Container (The Engine Blueprint)
This is where you declare the Manifest-level blueprints that dictate how the container configures itself.

[ ] Implement X11 GUI forwarding (not WSLg):

Helmsman does not install or depend on a WSL distro. GUI apps from the devcontainer reach the Windows host over **X11** (e.g. VcXsrv), not WSLg sockets.

In `/modules/devcontainer/.devcontainer/docker-compose.yml`, set `DISPLAY` to the host X server (already defaulted in `container-bashrc.sh`):

```yaml
environment:
  DISPLAY: ${DISPLAY:-host.docker.internal:0.0}
```

Host checklist:

- Run an X11 server on Windows (VcXsrv: disable native OpenGL, allow connections from Docker subnets).
- Start VcXsrv before launching GUI tools inside the container.
- Override `DISPLAY` in `.devcontainer/.env` if your X server uses a different host/port.
[ ] Map Cross-Repository Mounts:

Configure devcontainer.json to mount the sister directories (harness-builder, skills-repo, mcp-server) directly into the container's workspace paths, ensuring the code modified on Windows maps 1:1 inside the Linux sandbox.

[ ] Secure Token Injection Configuration:

Utilize the initializeCommand or standard Docker Compose environment passing within the devcontainer blueprint to automatically parse the host's .env variables and make them accessible to internal shell sessions.

Phase 3: Script the Terminal Level (In-Container Extensions)
This code lives as static scripts inside the Dev Container repository but is only executed on-demand at the Terminal level.

[ ] Write the Heavy Dependency Extensions:

Create a /scripts folder inside your Dev Container repository.

[ ] install_unity.sh: Script the automated headless installation of the Unity Hub and targeted editor versions.

[ ] install_matlab.sh: Script the silent installation patterns for MATLAB and its runtime libraries.

[ ] install_webtools.sh: Script your common network, scraping, and custom web utility setups.

[ ] Build an Extension Launcher:

Add a simple terminal menu or quick aliases inside the container's .bashrc (e.g., helmsman-extend-unity) so you can execute these heavy installers instantly with a single command whenever you switch to a machine that needs them.