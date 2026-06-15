"""Panel 1 — Git submodule status and init (see docs/panels.md)."""

from __future__ import annotations

import re
import subprocess
import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox, ttk


@dataclass(frozen=True)
class Submodule:
    name: str
    path: str
    url: str
    status_code: str  # space, -, +, U, or ? when unknown
    commit: str | None


STATUS_LABELS = {
    " ": ("Installed", "ready"),
    "-": ("Not initialized", "missing"),
    "+": ("Installed (ahead)", "warning"),
    "U": ("Merge conflict", "error"),
    "?": ("Unknown", "unknown"),
}


def parse_gitmodules(gitmodules_path: Path) -> list[tuple[str, str, str]]:
    """Return (name, path, url) tuples from .gitmodules."""
    if not gitmodules_path.is_file():
        return []

    text = gitmodules_path.read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^\[submodule ", text)
    entries: list[tuple[str, str, str]] = []

    for block in blocks[1:]:
        header, _, body = block.partition("]\n")
        name = header.strip().strip('"')
        path_match = re.search(r"(?m)^\s*path\s*=\s*(.+)$", body)
        url_match = re.search(r"(?m)^\s*url\s*=\s*(.+)$", body)
        if not path_match or not url_match:
            continue
        entries.append((name, path_match.group(1).strip(), url_match.group(1).strip()))

    return entries


def query_submodule_status(repo_root: Path) -> dict[str, tuple[str, str | None]]:
    """Map submodule path -> (status_code, short commit hash)."""
    result = subprocess.run(
        ["git", "submodule", "status"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return {}

    status_by_path: dict[str, tuple[str, str | None]] = {}
    for raw_line in result.stdout.splitlines():
        line = raw_line.rstrip("\r\n")
        if not line:
            continue
        code = line[0] if line[0] in "-+U " else "?"
        rest = line[1:].strip()
        parts = rest.split()
        if len(parts) < 2:
            continue
        commit, path = parts[0], parts[1]
        status_by_path[path] = (code, commit)
    return status_by_path


def load_submodules(repo_root: Path) -> list[Submodule]:
    gitmodules = repo_root / ".gitmodules"
    status_by_path = query_submodule_status(repo_root)
    submodules: list[Submodule] = []

    for name, path, url in parse_gitmodules(gitmodules):
        code, commit = status_by_path.get(path, ("?", None))
        if code == "?" and not (repo_root / path).exists():
            code = "-"
        submodules.append(
            Submodule(
                name=name,
                path=path,
                url=url,
                status_code=code,
                commit=commit,
            )
        )

    return submodules


def init_submodule(repo_root: Path, path: str) -> tuple[bool, str]:
    result = subprocess.run(
        ["git", "submodule", "update", "--init", "--", path],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output.strip()


class SubmodulesPanel(ttk.Frame):
    """Quick way to see and init Helmsman Git submodules."""

    def __init__(self, parent: tk.Misc, repo_root: Path) -> None:
        super().__init__(parent, padding=8)
        self.repo_root = repo_root
        self._rows: list[dict[str, tk.Misc]] = []
        self._busy = False

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(
            header,
            text="Git submodules",
            font=("", 11, "bold"),
        ).pack(side=tk.LEFT)

        ttk.Button(header, text="Refresh", command=self.refresh).pack(side=tk.RIGHT, padx=(4, 0))
        ttk.Button(header, text="Init all missing", command=self._init_all_missing).pack(
            side=tk.RIGHT
        )

        ttk.Label(
            self,
            text="Shows which core repositories are present under modules/. "
            "Use Init to clone and register a submodule that is not yet installed.",
            wraplength=680,
        ).pack(anchor="w", pady=(0, 8))

        columns = ("status", "name", "path", "commit")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=8,
            selectmode="browse",
        )
        self.tree.heading("status", text="Status")
        self.tree.heading("name", text="Module")
        self.tree.heading("path", text="Path")
        self.tree.heading("commit", text="Commit")
        self.tree.column("status", width=140, stretch=False)
        self.tree.column("name", width=120, stretch=False)
        self.tree.column("path", width=200, stretch=True)
        self.tree.column("commit", width=100, stretch=False)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.tag_configure("ready", foreground="#1a7f37")
        self.tree.tag_configure("warning", foreground="#9a6700")
        self.tree.tag_configure("missing", foreground="#cf222e")
        self.tree.tag_configure("error", foreground="#cf222e")
        self.tree.tag_configure("unknown", foreground="#656d76")

        actions = ttk.Frame(self)
        actions.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(actions, text="Init selected", command=self._init_selected).pack(side=tk.LEFT)

        ttk.Label(self, text="Output", font=("", 9, "bold")).pack(anchor="w", pady=(12, 4))
        self.output = tk.Text(self, height=8, wrap=tk.WORD, font=("Consolas", 9))
        output_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.output.yview)
        self.output.configure(yscrollcommand=output_scroll.set, state=tk.DISABLED)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _repo_root(self) -> Path:
        return self.repo_root

    def _append_output(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text.rstrip() + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        for child in self.winfo_children():
            try:
                child.configure(state=state)
            except tk.TclError:
                pass

    def refresh(self) -> None:
        repo = self._repo_root()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._rows.clear()

        if not (repo / ".git").exists():
            self._append_output(f"Not a git repository: {repo}")
            return

        submodules = load_submodules(repo)
        if not submodules:
            self._append_output("No submodules found in .gitmodules.")
            return

        for sub in submodules:
            label, tag = STATUS_LABELS.get(sub.status_code, STATUS_LABELS["?"])
            commit = sub.commit[:8] if sub.commit else "—"
            item_id = self.tree.insert(
                "",
                tk.END,
                values=(label, sub.name, sub.path, commit),
                tags=(tag,),
            )
            self._rows.append({"id": item_id, "path": sub.path, "status": sub.status_code})

    def _selected_path(self) -> str | None:
        selection = self.tree.selection()
        if not selection:
            return None
        values = self.tree.item(selection[0], "values")
        if len(values) < 3:
            return None
        return str(values[2])

    def _init_selected(self) -> None:
        path = self._selected_path()
        if not path:
            messagebox.showinfo("Init submodule", "Select a submodule row first.")
            return
        self._run_init([path])

    def _init_all_missing(self) -> None:
        missing = [row["path"] for row in self._rows if row["status"] == "-"]
        if not missing:
            messagebox.showinfo("Init submodules", "All submodules are already initialized.")
            return
        self._run_init(missing)

    def _run_init(self, paths: list[str]) -> None:
        if self._busy:
            return

        repo = self._repo_root()

        def worker() -> None:
            failures: list[str] = []
            for path in paths:
                self.after(0, lambda p=path: self._append_output(f"\n==> git submodule update --init {p}"))
                ok, output = init_submodule(repo, path)
                if output:
                    self.after(0, lambda text=output: self._append_output(text))
                if not ok:
                    failures.append(path)

            def finish() -> None:
                self._set_busy(False)
                self.refresh()
                if failures:
                    messagebox.showerror(
                        "Init failed",
                        "Could not initialize:\n" + "\n".join(failures),
                    )
                elif len(paths) == 1:
                    messagebox.showinfo("Init complete", f"Initialized {paths[0]}.")
                else:
                    messagebox.showinfo("Init complete", f"Initialized {len(paths)} submodule(s).")

            self.after(0, finish)

        self._set_busy(True)
        threading.Thread(target=worker, daemon=True).start()
