---
name: create-hfeature
description: Scaffolds a new hFeature in fPool with master.md and decisions.md. Use when the user wants to create a feature in fPool, add an hFeature, start a new feature pool entry, or scaffold feature-pool documents from a prompt.
disable-model-invocation: true
---

# Create hFeature

Scaffold a new hFeature in `fPool/`: a three-word hyphenated folder containing `master.md` (section headers only) and an empty `decisions.md`. Ground truth: [canon-lnk/instructions/init_fPool.md](canon-lnk/instructions/init_fPool.md).

`canon-lnk` is a junction to the Helmsman canon. Read and copy seeded docs from there; do not read from `canon/` directly.

## Scope — do only this

When this skill is invoked, the agent's job is **only** to derive the folder name and create the scaffold. Do **not** implement the feature, fill in document content from the prompt, or edit unrelated files.

## Parse user input

Extract a **feature name** from the user's message (text after the skill invocation).

1. Strip optional leading filler: `new`, `a`, `an`, `create`, `add`, `feature`, `hfeature`.
2. Derive **three lowercase words** that summarize the feature.
3. Join them with hyphens for the folder name (e.g. `auto-ingest-easies`).

| Input | Folder name |
|-------|-------------|
| `auto ingest easies` | `auto-ingest-easies` |
| `helmsman source control` | `helmsman-source-control` |
| `dark mode toggle for settings` | `dark-mode-toggle` |

If the prompt does not contain enough context to pick three meaningful words, ask the user for a short feature name. Do not guess.

## Documents to create

Inside `fPool/<three-word-name>/`, follow [init_fPool.md](canon-lnk/instructions/init_fPool.md):

| File | Contents |
|------|----------|
| `master.md` | Section headers only — copy from the `<master.md>` default content in [canon-lnk/instructions/init_fPool.md](canon-lnk/instructions/init_fPool.md) |
| `decisions.md` | Empty |

## Workflow

```
Task progress:
- [ ] Step 1: Read init_fPool.md
- [ ] Step 2: Parse input and derive the three-word folder name
- [ ] Step 3: Create fPool/ if it does not exist
- [ ] Step 4: Create the feature folder and documents
- [ ] Step 5: Report what was created
```

### Step 1: Read init_fPool.md

Read [canon-lnk/instructions/init_fPool.md](canon-lnk/instructions/init_fPool.md) for the target structure and default `master.md` / `decisions.md` content.

### Step 2: Parse input

Derive the three-word hyphenated folder name from the user's prompt.

### Step 3: Ensure fPool exists

Create `fPool/` at the repo root if it does not exist.

### Step 4: Create the feature folder and documents

Create `fPool/<three-word-name>/` and write:

- `master.md` — copy the `<master.md>` section headers from [init_fPool.md](canon-lnk/instructions/init_fPool.md) verbatim
- `decisions.md` — create as an empty file

### Step 5: Report

List the folder and files created with their paths.

## Constraints

- Always start from [init_fPool.md](canon-lnk/instructions/init_fPool.md).
- Do **not** overwrite an existing feature folder or its files. If `fPool/<three-word-name>/` already exists, stop and report the conflict.
- `master.md` MUST contain only the section headers from the instruction default content. Do not pre-fill content from the user's prompt.
- `decisions.md` MUST be empty.
- Do not create additional files beyond `master.md` and `decisions.md`.
- Do not implement, code, or start work on the feature described in the prompt.
