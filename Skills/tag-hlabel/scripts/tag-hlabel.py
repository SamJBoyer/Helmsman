#!/usr/bin/env python3
"""Return the emoji for a taken hLabel matched by name or keyword."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TAKEN_LINE = re.compile(
    r"^\[X\]:\s+(?P<emoji>\S+)\s+#(?P<hex>[0-9A-Fa-f]{6}),\s+(?P<label>[^,]+),\s+(?P<usage>.*)$"
)


def find_glossary(path: Path | None) -> Path:
    if path is not None:
        if not path.is_file():
            raise FileNotFoundError(f"Glossary not found: {path}")
        return path

    for candidate in (
        Path("hDocs/glossary.md"),
        Path("docs/glossary.md"),
        Path.cwd() / "hDocs" / "glossary.md",
        Path.cwd() / "docs" / "glossary.md",
    ):
        if candidate.is_file():
            return candidate

    raise FileNotFoundError("Could not find hDocs/glossary.md or docs/glossary.md.")


def parse_taken_hlabels(glossary: Path) -> list[dict[str, str]]:
    text = glossary.read_text(encoding="utf-8")
    start = text.find("# hLabels")
    if start == -1:
        raise ValueError("Glossary has no # hLabels section.")

    section = text[start:].split("---", 1)[0]
    entries: list[dict[str, str]] = []

    for line in section.splitlines():
        match = TAKEN_LINE.match(line.strip())
        if not match:
            continue
        entries.append(
            {
                "emoji": match.group("emoji"),
                "hex": f"#{match.group('hex').upper()}",
                "label": match.group("label").strip(),
                "usage": match.group("usage").strip(),
            }
        )

    if not entries:
        raise ValueError("No taken hLabels found. Claim a label in the glossary first.")

    return entries


def score_match(query: str, entry: dict[str, str]) -> int:
    q = query.casefold()
    label = entry["label"].casefold()
    usage = entry["usage"].casefold()

    if q == label:
        return 100
    if label.startswith(q) or q.startswith(label):
        return 80
    if q in label:
        return 60
    if q in usage:
        return 40
    label_words = {word for word in re.split(r"[\s\-_/]+", label) if word}
    query_words = {word for word in re.split(r"[\s\-_/]+", q) if word}
    if query_words and query_words <= label_words:
        return 50
    return 0


def find_matches(query: str, entries: list[dict[str, str]]) -> list[dict[str, str]]:
    scored = [(score_match(query, entry), entry) for entry in entries]
    best = max((score for score, _ in scored), default=0)
    if best == 0:
        return []
    return [entry for score, entry in scored if score == best]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="hLabel name or keyword to match")
    parser.add_argument(
        "--glossary",
        type=Path,
        default=None,
        help="Path to glossary.md (default: hDocs/glossary.md)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print label and usage details instead of emoji only",
    )
    args = parser.parse_args()

    query = args.query.strip()
    if not query:
        print("error: query is required", file=sys.stderr)
        return 1

    try:
        glossary = find_glossary(args.glossary)
        entries = parse_taken_hlabels(glossary)
        matches = find_matches(query, entries)
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not matches:
        print(f"error: no taken hLabel matches {query!r}", file=sys.stderr)
        return 1

    if len(matches) > 1:
        print("error: multiple hLabels match:", file=sys.stderr)
        for entry in matches:
            print(f"  {entry['emoji']} {entry['label']}", file=sys.stderr)
        return 2

    entry = matches[0]
    if args.verbose:
        print(f"{entry['emoji']} {entry['label']} — {entry['usage']}")
    else:
        print(entry["emoji"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
