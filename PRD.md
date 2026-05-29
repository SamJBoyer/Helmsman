# Product Requirements Document

## Overview

Helmsman tracks small deliverables as issues under `.issues/`. Agents pick the highest-priority open item, implement it, validate with tests, update this PRD, and log notes in `progress.txt`.

## Requirements

| ID | Priority | Status | Description |
|----|----------|--------|-------------|
| i1 | 1 (first) | **Done** | Python script named `hello_world.py` that prints `hello world`. |
| i2 | 2 | **Done** | MATLAB script that prints `hello world` and can be executed. |
| i3 | 3 (last) | **Done** | Python script that computes `1 + 2` and prints the result. |

## Completed work

### i1 — Python hello world (2026-05-29)

- Added `hello_world.py` with a `main()` entry point that prints `hello world`.
- Validation: `./test.sh validate` runs the script and checks stdout.

### i2 — MATLAB hello world (2026-05-29)

- Added `hello_world.m` that uses `disp('hello world')`.
- Execution: run with Octave (`octave --quiet hello_world.m`) or MATLAB (`matlab -batch "run('hello_world.m')"`).
- Validation: `./test.sh validate` runs the script via Octave and checks stdout.

### i3 — Python addition (2026-05-29)

- Added `add_one_two.py` with a `main()` entry point that prints `1 + 2` (result `3`).
- Validation: `./test.sh validate` runs the script and checks stdout.

## Remaining work

None — all issues (i1, i2, i3) are complete.
