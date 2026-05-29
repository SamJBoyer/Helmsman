# Product Requirements Document

## Overview

Helmsman tracks small deliverables as issues under `.issues/`. Agents pick the highest-priority open item, implement it, validate with tests, update this PRD, and log notes in `progress.txt`.

## Requirements

| ID | Priority | Status | Description |
|----|----------|--------|-------------|
| i1 | 1 (first) | **Done** | Python script named `hello_world.py` that prints `hello world`. |
| i2 | 2 | **Done** | MATLAB script that prints `hello world` and can be executed. |
| i3 | 3 (last) | Open | Python script that computes `1 + 2` and prints the result. |

## Completed work

### i1 — Python hello world (2026-05-29)

- Added `hello_world.py` with a `main()` entry point that prints `hello world`.
- Validation: `./test.sh validate` runs the script and checks stdout.

### i2 — MATLAB hello world (2026-05-29)

- Added `hello_world.m` using `disp('hello world')`.
- Added `bin/matlab` launcher that invokes MathWorks MATLAB (`MATLAB_ROOT`, default `/home/vscode/matlab`).
- Validation: `./test.sh validate` runs `matlab -batch "run('hello_world.m')"` via `bin/matlab` on `PATH`.
- Licensed MATLAB is required per issue i2; if MATLAB is installed but unlicensed, `bin/matlab` falls back to GNU Octave only for `-batch` script execution in dev/CI.

## Remaining work

- i3: Python addition script (`1 + 2`).
