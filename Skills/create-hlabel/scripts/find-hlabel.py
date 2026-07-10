#!/usr/bin/env python3
"""Find the closest available hLabel for a given color in docs/glossary.md."""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

HLABEL_LINE = re.compile(
    r"^\[ \]:\s+(?P<emoji>\S+)\s+#(?P<hex>[0-9A-Fa-f]{6}),\s+\[label\],\s+\[useage\]\s*$"
)
HEX_COLOR = re.compile(r"^#?([0-9A-Fa-f]{6})$")
RGB_COLOR = re.compile(
    r"^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$", re.IGNORECASE
)

NAMED_COLORS = {
    "red": (234, 67, 53),
    "orange": (255, 109, 1),
    "yellow": (251, 188, 4),
    "green": (52, 168, 83),
    "blue": (66, 133, 244),
    "purple": (147, 52, 233),
    "brown": (161, 66, 54),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}


def parse_color(value: str) -> tuple[int, int, int]:
    value = value.strip()

    if (match := HEX_COLOR.match(value)):
        hex_value = match.group(1)
        return (
            int(hex_value[0:2], 16),
            int(hex_value[2:4], 16),
            int(hex_value[4:6], 16),
        )

    if (match := RGB_COLOR.match(value)):
        parts = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        if any(part < 0 or part > 255 for part in parts):
            raise ValueError(f"RGB values must be 0-255: {value}")
        return parts

    key = value.lower()
    if key in NAMED_COLORS:
        return NAMED_COLORS[key]

    raise ValueError(
        f"Unsupported color format: {value!r}. Use #RRGGBB, RRGGBB, rgb(r,g,b), or a basic color name."
    )


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def find_glossary(path: Path | None) -> Path:
    if path is not None:
        if not path.is_file():
            raise FileNotFoundError(f"Glossary not found: {path}")
        return path

    for candidate in (Path("docs/glossary.md"), Path.cwd() / "docs" / "glossary.md"):
        if candidate.is_file():
            return candidate

    raise FileNotFoundError("Could not find docs/glossary.md from the current directory.")


def parse_available_hlabels(glossary: Path) -> list[dict[str, str]]:
    text = glossary.read_text(encoding="utf-8")
    start = text.find("# hLabels")
    if start == -1:
        raise ValueError("Glossary has no # hLabels section.")

    section = text[start:].split("---", 1)[0]
    entries: list[dict[str, str]] = []

    for line in section.splitlines():
        match = HLABEL_LINE.match(line.strip())
        if not match:
            continue
        entries.append(
            {
                "emoji": match.group("emoji"),
                "hex": f"#{match.group('hex').upper()}",
                "rgb": parse_color(match.group("hex")),
            }
        )

    if not entries:
        raise ValueError("No available hLabels found. All slots may be taken ([X]).")

    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("color", help="Target color: #RRGGBB, rgb(r,g,b), or a basic color name")
    parser.add_argument(
        "--glossary",
        type=Path,
        default=None,
        help="Path to glossary.md (default: docs/glossary.md)",
    )
    args = parser.parse_args()

    try:
        target = parse_color(args.color)
        glossary = find_glossary(args.glossary)
        entries = parse_available_hlabels(glossary)
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    best_distance = min(color_distance(target, entry["rgb"]) for entry in entries)
    matches = [entry for entry in entries if color_distance(target, entry["rgb"]) == best_distance]

    print(f"target: rgb{target}")
    print(f"glossary: {glossary}")
    print(f"distance: {best_distance:.2f}")
    for entry in matches:
        print(f"match: {entry['emoji']} {entry['hex']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
