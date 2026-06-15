"""Host-side dev container build and status checks."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

DEFAULT_IMAGE = "dev-cli:local"
CONTAINER_NAME = "dev-container"


def devcontainer_module_root(repo_root: Path) -> Path:
    return repo_root / "modules" / "devcontainer"


def compose_dir(repo_root: Path) -> Path:
    return devcontainer_module_root(repo_root) / ".devcontainer"


def is_devcontainer_running() -> bool:
    result = subprocess.run(
        [
            "docker",
            "ps",
            "--filter",
            f"name=^{CONTAINER_NAME}$",
            "--filter",
            "status=running",
            "--format",
            "{{.Names}}",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return False
    return CONTAINER_NAME in result.stdout.splitlines()


def _run_logged(
    cmd: list[str],
    cwd: Path,
    on_line: Callable[[str], None] | None = None,
) -> tuple[bool, str]:
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    lines: list[str] = []
    assert process.stdout is not None
    for line in process.stdout:
        stripped = line.rstrip()
        lines.append(stripped)
        if on_line:
            on_line(stripped)
    process.wait()
    output = "\n".join(lines).strip()
    return process.returncode == 0, output


def build_devcontainer(
    repo_root: Path,
    on_line: Callable[[str], None] | None = None,
) -> tuple[bool, str]:
    module_root = devcontainer_module_root(repo_root)
    build_script = module_root / "scripts" / "build-image.ps1"

    if build_script.is_file():
        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(build_script),
        ]
        cwd = module_root
    else:
        cmd = [
            "docker",
            "build",
            "--platform",
            "linux/amd64",
            "-t",
            DEFAULT_IMAGE,
            "-f",
            "Dockerfile",
            ".",
        ]
        cwd = module_root

    if not cwd.is_dir():
        return False, f"Devcontainer module not found: {cwd}"

    return _run_logged(cmd, cwd, on_line)


def up_devcontainer(
    repo_root: Path,
    on_line: Callable[[str], None] | None = None,
) -> tuple[bool, str]:
    compose = compose_dir(repo_root)
    if not compose.is_dir():
        return False, f"Compose project not found: {compose}"

    cmd = ["docker", "compose", "up", "-d"]
    return _run_logged(cmd, compose, on_line)


def build_and_up_devcontainer(
    repo_root: Path,
    on_line: Callable[[str], None] | None = None,
) -> tuple[bool, str]:
    ok, output = build_devcontainer(repo_root, on_line)
    if not ok:
        return False, output

    if on_line:
        on_line("\n==> docker compose up -d")

    up_ok, up_output = up_devcontainer(repo_root, on_line)
    if not up_ok:
        combined = "\n\n".join(part for part in (output, up_output) if part)
        return False, combined

    combined = "\n\n".join(part for part in (output, up_output) if part)
    return True, combined
