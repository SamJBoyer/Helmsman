---
name: pool-feature
description: Takes an existing feature iticket from `.scratch/.itickets/feature/` and creates a per-feature workspace folder in `fpool/` at the repo root, seeded with a copy of that feature's issue. Use when the user wants to pool a feature, open a feature workspace, move a feature into fpool, or start working a feature in its own workspace.
disable-model-invocation: true
---

# Pool Feature

Give a feature its own workspace where the actual work is done. This skill takes a
**feature iticket** that already exists in `.scratch/.itickets/feature/` and creates a
folder for it in **fpool** (the feature pool at the repo root), seeded with a copy of
that feature's issue.

- **fpool** — `fpool/` at the repo root. One subfolder per feature workspace.
- The source feature iticket **stays in place** in `.scratch/.itickets/feature/`; it
  remains the tracker. fpool holds the working copy.

Feature iticket file format: [ITICKET-FORMAT.md](../itickets/ITICKET-FORMAT.md).
The `feature` itag is defined in the `<itag>` section of [glossary.md](../../../docs/glossary.md).

## Parse user input

Extract the **target feature** from the user's message (text after the skill invocation).
Strip optional leading filler: `pool`, `open`, `start`, `feature`.

The remaining text identifies one feature iticket. Accept any of:

| Input | Interpreted as |
|-------|----------------|
| `per-feature-workspace` | local filename `per-feature-workspace.md` |
| `hotlink system` | description / title fragment |
| `8` or a GitHub URL | `github-issue:` value |

If no target can be parsed, list the available features and ask the user to pick one:

```bash
ls .scratch/.itickets/feature/*.md
```

## Workflow

```
Task progress:
- [ ] Step 1: Resolve the target feature iticket
- [ ] Step 2: Derive the workspace folder name
- [ ] Step 3: Create fpool/<name>/
- [ ] Step 4: Seed the workspace with the issue
- [ ] Step 5: Report
```

### Step 1: Resolve the target feature iticket

Find exactly one `.md` file in `.scratch/.itickets/feature/`:

- **Filename** — match `.scratch/.itickets/feature/<name>.md` directly.
- **Issue number or URL** — match the file whose `github-issue:` line equals it per the
  [matching rule](../itickets/ITICKET-FORMAT.md#matching-rule).
- **Description / title fragment** — read the feature files and pick the best match.

If multiple files match, ask the user to pick one. If none match, stop and report that no
feature iticket was found. If the feature exists on GitHub but has no local file, tell the
user to run `sync-iticket feature` first — this skill only pools locally-tracked features.

### Step 2: Derive the workspace folder name

Use the source iticket's filename **stem** (the name without `.md`) as the workspace folder
name. Example: `per-feature-workspace.md` → `fpool/per-feature-workspace/`.

### Step 3: Create fpool/<name>/

Create `fpool/` at the repo root if it does not exist (lazily — only when pooling the first
feature). Then create `fpool/<name>/`.

If `fpool/<name>/` already exists, stop and report that the feature is already pooled. Do
**not** overwrite an existing workspace.

### Step 4: Seed the workspace with the issue

Copy the source feature iticket into the new folder as `issue.md`, preserving its contents
verbatim (`description:` and `github-issue:` lines). Leave the original file untouched in
`.scratch/.itickets/feature/`.

### Step 5: Report

Report a brief summary: feature name, source file, and the created `fpool/<name>/issue.md`.

## Constraints

- Do **not** delete, move, or edit the source iticket in `.scratch/.itickets/feature/`.
- Do **not** create, close, or edit GitHub issues.
- Do **not** overwrite an existing `fpool/<name>/` workspace.
- Do **not** scaffold extra files — seed only `issue.md`.
- Only pool features that have a local iticket file; never invent one.
