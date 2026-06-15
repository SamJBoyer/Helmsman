#!/usr/bin/env python3
"""
Helmsman host GUI — panels for repo orchestration on the Windows host.

Stdlib only (tkinter); no pip dependencies.
"""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

_GUIS_DIR = Path(__file__).resolve().parent
if str(_GUIS_DIR) not in sys.path:
    sys.path.insert(0, str(_GUIS_DIR))

from panels.manifest import ManifestPanel
from panels.submodules import SubmodulesPanel
from upper import UpperSection, default_mount_root


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


class HelmsmanApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Helmsman")
        self.geometry("820x680")
        self.minsize(720, 520)

        self.mount_root = tk.StringVar(value=str(default_mount_root()))

        self._build_ui()

    def _build_ui(self) -> None:
        upper = UpperSection(self, self.mount_root, repo_root())
        upper.pack(fill=tk.X)

        notebook = ttk.Notebook(self, padding=8)
        notebook.pack(fill=tk.BOTH, expand=True)

        submodules = SubmodulesPanel(notebook, repo_root())
        manifest = ManifestPanel(notebook, self.mount_root)

        notebook.add(submodules, text="Panel 1 — Submodules")
        notebook.add(manifest, text="Manifest")

        self.bind("<Control-r>", lambda _e: submodules.refresh())


def main() -> None:
    app = HelmsmanApp()
    app.mainloop()


if __name__ == "__main__":
    main()
