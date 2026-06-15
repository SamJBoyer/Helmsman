"""Upper section — universal host controls (see docs/layout.md)."""

from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from devcontainer_host import build_and_up_devcontainer, is_devcontainer_running


def default_mount_root() -> Path:
    return Path.home() / "Desktop" / "Development"


class UpperSection(ttk.Frame):
    """Top toolbar: mount root on the left, updev + status lamp on the right."""

    LAMP_RUNNING = "#22c55e"
    LAMP_STOPPED = "#ef4444"
    LAMP_WORKING = "#eab308"

    def __init__(self, parent: tk.Misc, mount_root: tk.StringVar, repo_root: Path) -> None:
        super().__init__(parent, padding=(8, 8, 8, 0))
        self.mount_root = mount_root
        self.repo_root = repo_root
        self._updev_busy = False
        self._poll_interval_ms = 3000

        self._build_ui()
        self._refresh_lamp()
        self.after(self._poll_interval_ms, self._poll_status)

    def _build_ui(self) -> None:
        ttk.Label(self, text="Mount root:").pack(side=tk.LEFT)
        ttk.Entry(self, textvariable=self.mount_root, width=48).pack(
            side=tk.LEFT, padx=(4, 8)
        )
        ttk.Button(self, text="Browse…", command=self._browse_mount_root).pack(side=tk.LEFT)

        ttk.Frame(self).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.lamp = tk.Canvas(self, width=18, height=18, highlightthickness=0, bd=0)
        self.lamp.pack(side=tk.RIGHT, padx=(8, 0))
        self._lamp_oval = self.lamp.create_oval(
            2, 2, 16, 16, fill=self.LAMP_STOPPED, outline="#1f2937"
        )

        self.updev_btn = ttk.Button(self, text="updev", command=self._run_updev)
        self.updev_btn.pack(side=tk.RIGHT, padx=(8, 0))

    def _set_lamp(self, color: str) -> None:
        self.lamp.itemconfigure(self._lamp_oval, fill=color)

    def _refresh_lamp(self) -> None:
        if self._updev_busy:
            self._set_lamp(self.LAMP_WORKING)
            return
        running = is_devcontainer_running()
        self._set_lamp(self.LAMP_RUNNING if running else self.LAMP_STOPPED)

    def _poll_status(self) -> None:
        self._refresh_lamp()
        self.after(self._poll_interval_ms, self._poll_status)

    def _browse_mount_root(self) -> None:
        initial = self.mount_root.get().strip() or str(default_mount_root())
        chosen = filedialog.askdirectory(initialdir=initial)
        if chosen:
            self.mount_root.set(chosen)

    def _run_updev(self) -> None:
        if self._updev_busy:
            return

        self._updev_busy = True
        self.updev_btn.configure(state=tk.DISABLED)
        self._set_lamp(self.LAMP_WORKING)

        def worker() -> None:
            ok, output = build_and_up_devcontainer(self.repo_root)

            def finish() -> None:
                self._updev_busy = False
                self.updev_btn.configure(state=tk.NORMAL)
                self._refresh_lamp()
                if ok:
                    messagebox.showinfo("updev", "Dev container image built and started.")
                else:
                    detail = output[-4000:] if len(output) > 4000 else output
                    messagebox.showerror("updev failed", detail or "Build or compose failed.")

            self.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()
