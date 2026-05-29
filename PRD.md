# Product Requirements Document

## Overview

Helmsman tracks small deliverables as issues under `.issues/`. Agents pick the highest-priority open item, implement it, validate with tests, update this PRD, and log notes in `progress.txt`.

## Requirements

| ID | Priority | Status | Description |
|----|----------|--------|-------------|
| i1 | 1 (first) | **Done** | Python script named `hello_world.py` that prints `hello world`. |
| i2 | 2 | Open | MATLAB script that prints `hello world` and can be executed. |
| i3 | 3 (last) | Open | Python script that computes `1 + 2` and prints the result. |

## Completed work

### i1 — Python hello world (2026-05-29)

- Added `hello_world.py` with a `main()` entry point that prints `hello world`.
- Validation: `./test.sh validate` runs the script and checks stdout.

## Remaining work

- i2: MATLAB hello world script and execution path.
- i3: Python addition script (`1 + 2`).
