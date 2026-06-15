"""Manifest editor panel — Manifest Conductor blueprint (see docs/addons.md)."""

from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

MANIFEST_VERSION = 1


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


DEFAULT_MODULES = {
    "devcontainer": "modules/devcontainer",
    "mcp-server": "modules/mcp-server",
    "harness-builder": "modules/harness-builder",
    "skills-repo": "modules/skills-repo",
}


def dump_yaml(value: Any, indent: int = 0) -> str:
    """Minimal YAML emitter for manifest dicts (stdlib-only)."""
    pad = "  " * indent
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if not value:
            return '""'
        if "\n" in value:
            lines = value.splitlines()
            inner = "\n".join(f"{'  ' * (indent + 1)}{line}" for line in lines)
            return "|\n" + inner
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        if any(c in value for c in ":{}[]&*#?|-<>=!%@`") or value.startswith((" ", "\t")):
            return f'"{escaped}"'
        return value
    if isinstance(value, list):
        if not value:
            return "[]"
        lines: list[str] = []
        for item in value:
            rendered = dump_yaml(item, indent + 1)
            if isinstance(item, dict):
                lines.append(f"{pad}- {rendered.lstrip()}")
            else:
                lines.append(f"{pad}- {rendered}")
        return "\n".join(lines)
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = []
        for key, item in value.items():
            rendered = dump_yaml(item, indent + 1)
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{pad}{key}:")
                lines.append(rendered)
            else:
                lines.append(f"{pad}{key}: {rendered}")
        return "\n".join(lines)
    return json.dumps(value)


def build_manifest(state: dict[str, Any]) -> dict[str, Any]:
    modules: dict[str, Any] = {}
    for name, cfg in state["modules"].items():
        if not cfg["enabled"].get():
            continue
        modules[name] = {"path": cfg["path"].get().strip()}

    dev_image = state["dev_image"].get().strip() or "dev-cli:local"

    cross_repo = [
        name
        for name, cfg in state["modules"].items()
        if name != "devcontainer" and cfg["enabled"].get()
    ]

    return {
        "version": MANIFEST_VERSION,
        "name": state["manifest_name"].get().strip() or "helmsman",
        "host": {
            "root": state["root_path"].get().strip() or ".",
            "modules": modules,
        },
        "devcontainer": {
            "image": dev_image,
            "display": state["display"].get().strip() or "host.docker.internal:0.0",
            "host_licenses": state["host_licenses"].get().strip() or None,
            "mounts": {
                "development": {
                    "host": state["mount_host"].get().strip()
                    or "${USERPROFILE}/Desktop/Development",
                    "container": "/workspaces/development",
                },
            },
            "cross_repo_modules": cross_repo,
        },
        "extensions": {
            "install_scripts": {
                "unity": {
                    "enabled": state["ext_unity"].get(),
                    "script": "scripts/install_unity.sh",
                },
                "matlab": {
                    "enabled": state["ext_matlab"].get(),
                    "script": "scripts/install_matlab.sh",
                },
                "webtools": {
                    "enabled": state["ext_webtools"].get(),
                    "script": "scripts/install_webtools.sh",
                },
            },
        },
    }


class ManifestPanel(ttk.Frame):
    """Edit and save helmsman.manifest.yaml."""

    def __init__(self, parent: tk.Misc, mount_root: tk.StringVar) -> None:
        super().__init__(parent, padding=4)
        self.mount_root = mount_root

        self.state: dict[str, Any] = {
            "manifest_name": tk.StringVar(value="helmsman"),
            "dev_image": tk.StringVar(value="dev-cli:local"),
            "display": tk.StringVar(value="host.docker.internal:0.0"),
            "host_licenses": tk.StringVar(value=""),
            "ext_unity": tk.BooleanVar(value=False),
            "ext_matlab": tk.BooleanVar(value=False),
            "ext_webtools": tk.BooleanVar(value=False),
            "modules": {},
        }

        self._build_ui()
        self._bind_preview_updates()
        self.refresh_preview()

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self, padding=(0, 0, 0, 8))
        toolbar.pack(fill=tk.X)

        ttk.Label(toolbar, text="Manifest name:").pack(side=tk.LEFT)
        ttk.Entry(toolbar, textvariable=self.state["manifest_name"], width=18).pack(
            side=tk.LEFT, padx=(4, 0)
        )

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        notebook.add(self._build_modules_tab(), text="Phase 1 — Modules")
        notebook.add(self._build_devcontainer_tab(), text="Phase 2 — Devcontainer")
        notebook.add(self._build_extensions_tab(), text="Phase 3 — Extensions")
        notebook.add(self._build_preview_tab(), text="Preview")

        actions = ttk.Frame(self, padding=(0, 8, 0, 0))
        actions.pack(fill=tk.X)
        ttk.Button(actions, text="Save manifest.yaml", command=self.save_manifest).pack(
            side=tk.RIGHT
        )
        ttk.Button(actions, text="Save As…", command=self.save_manifest_as).pack(
            side=tk.RIGHT, padx=(0, 8)
        )
        ttk.Button(actions, text="Refresh preview", command=self.refresh_preview).pack(
            side=tk.LEFT
        )

    def _scrollable(self, parent: ttk.Frame) -> tuple[tk.Canvas, ttk.Frame]:
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind(
            "<Configure>",
            lambda _e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return canvas, inner

    def _build_modules_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self)
        _canvas, inner = self._scrollable(frame)

        ttk.Label(
            inner,
            text="Core repositories (Git submodules)",
            font=("", 10, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        headers = ("Enable", "Module", "Path")
        for col, text in enumerate(headers):
            ttk.Label(inner, text=text, font=("", 9, "bold")).grid(
                row=1, column=col, sticky="w", padx=(0, 8)
            )

        for row_idx, (name, default_path) in enumerate(DEFAULT_MODULES.items(), start=2):
            enabled = tk.BooleanVar(value=True)
            path = tk.StringVar(value=default_path)
            self.state["modules"][name] = {
                "enabled": enabled,
                "path": path,
            }
            ttk.Checkbutton(inner, variable=enabled).grid(row=row_idx, column=0, sticky="w")
            ttk.Label(inner, text=name).grid(row=row_idx, column=1, sticky="w", padx=(0, 8))
            ttk.Entry(inner, textvariable=path, width=40).grid(
                row=row_idx, column=2, sticky="ew", padx=(0, 8)
            )

        inner.columnconfigure(2, weight=1)
        return frame

    def _build_devcontainer_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self)
        _canvas, inner = self._scrollable(frame)

        ttk.Label(
            inner,
            text="Manifest-level devcontainer blueprint",
            font=("", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        fields = [
            ("DEV_IMAGE:", self.state["dev_image"]),
            ("DISPLAY:", self.state["display"]),
            ("HOST_LICENSES (optional):", self.state["host_licenses"]),
        ]
        for row_idx, (label, var) in enumerate(fields, start=1):
            ttk.Label(inner, text=label).grid(row=row_idx, column=0, sticky="w", pady=3)
            ttk.Entry(inner, textvariable=var, width=48).grid(
                row=row_idx, column=1, sticky="ew", pady=3
            )

        ttk.Label(
            inner,
            text="X11 forwarding uses VcXsrv on the Windows host (not WSLg). "
            "The development mount host path is set via Mount root in the toolbar. "
            "Heavy deps (Unity, MATLAB) are configured under Phase 3 — Extensions.",
            wraplength=520,
        ).grid(row=len(fields) + 1, column=0, columnspan=2, sticky="w", pady=(12, 0))

        inner.columnconfigure(1, weight=1)
        return frame

    def _build_extensions_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)
        ttk.Label(
            frame,
            text="In-container heavy dependency installers (on-demand scripts)",
            font=("", 10, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        for label, var in (
            ("install_unity.sh — Unity Hub + editor versions", self.state["ext_unity"]),
            ("install_matlab.sh — MATLAB silent install", self.state["ext_matlab"]),
            ("install_webtools.sh — network / scraping utilities", self.state["ext_webtools"]),
        ):
            ttk.Checkbutton(frame, text=label, variable=var).pack(anchor="w", pady=4)

        ttk.Label(
            frame,
            text="These scripts live under modules/devcontainer/scripts/ and are run "
            "from the container terminal (e.g. helmsman-extend-unity aliases).",
            wraplength=560,
        ).pack(anchor="w", pady=(16, 0))
        return frame

    def _build_preview_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=4)
        self.preview = tk.Text(frame, wrap=tk.NONE, font=("Consolas", 10))
        yscroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.preview.yview)
        xscroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.preview.xview)
        self.preview.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        return frame

    def _bind_preview_updates(self) -> None:
        tracked = [
            self.state["manifest_name"],
            self.mount_root,
            self.state["dev_image"],
            self.state["display"],
            self.state["host_licenses"],
            self.state["ext_unity"],
            self.state["ext_matlab"],
            self.state["ext_webtools"],
        ]
        for var in tracked:
            var.trace_add("write", lambda *_: self.refresh_preview())
        for cfg in self.state["modules"].values():
            for var in cfg.values():
                var.trace_add("write", lambda *_: self.refresh_preview())

    def _manifest_state(self) -> dict[str, Any]:
        return {
            **self.state,
            "root_path": tk.StringVar(value=str(repo_root())),
            "mount_host": self.mount_root,
        }

    def manifest_text(self) -> str:
        data = build_manifest(self._manifest_state())
        header = (
            "# Helmsman manifest — Manifest Conductor blueprint\n"
            "# Generated by guis/helmsman.py (see docs/addons.md)\n\n"
        )
        return header + dump_yaml(data) + "\n"

    def refresh_preview(self) -> None:
        self.preview.delete("1.0", tk.END)
        self.preview.insert("1.0", self.manifest_text())

    def _default_output_path(self) -> Path:
        return repo_root() / "helmsman.manifest.yaml"

    def save_manifest(self) -> None:
        path = self._default_output_path()
        try:
            path.write_text(self.manifest_text(), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))
            return
        messagebox.showinfo("Saved", f"Wrote {path}")

    def save_manifest_as(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save manifest as",
            initialdir=str(repo_root()),
            initialfile="helmsman.manifest.yaml",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            Path(path).write_text(self.manifest_text(), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))
            return
        messagebox.showinfo("Saved", f"Wrote {path}")
