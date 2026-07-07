---
name: setup-helmsman
description: Scaffold a new Helmsman project by creating HELMSMAN.md in the repo root and the standard docs/ documents. All docs are created empty except glossary.md, which is seeded with the itag definitions. Use when the user asks to set up Helmsman, scaffold Helmsman docs, or initialize a new Helmsman project.
disable-model-invocation: true
---

# Setup Helmsman

Scaffold the Helmsman document structure for a project: a `HELMSMAN.md` guide in the repo root plus the standard `docs/` documents. Every doc is created **empty** except `glossary.md`, which is seeded with the itag definitions.

## Documents to create

Create these in `docs/` (all empty unless noted):

| File | Contents |
|------|----------|
| `glossary.md` | Seeded from [templates/glossary.md](templates/glossary.md) (itag definitions) |
| `git-tech.md` | empty |
| `wants.md` | empty |
| `high-level.md` | empty |
| `status.md` | empty |
| `overlay.md` | empty |
| `questions.md` | empty |
| `artifacts.md` | empty |
| `ehan.md` | empty |

Also create `HELMSMAN.md` in the **repo root** from [templates/HELMSMAN.md](templates/HELMSMAN.md).

## Workflow

```
Task progress:
- [ ] Step 1: Create HELMSMAN.md in the repo root
- [ ] Step 2: Create docs/glossary.md seeded with itag definitions
- [ ] Step 3: Create the remaining docs as empty files
- [ ] Step 4: Report what was created
```

### Step 1: Create HELMSMAN.md

Copy [templates/HELMSMAN.md](templates/HELMSMAN.md) verbatim to `HELMSMAN.md` in the repo root.

### Step 2: Create docs/glossary.md

Copy [templates/glossary.md](templates/glossary.md) verbatim to `docs/glossary.md`. This is the only doc with starting content.

### Step 3: Create the remaining docs

Create each remaining file in the table above as an empty file. Create the `docs/` directory first if it does not exist.

### Step 4: Report

List the files created and their paths.

## Constraints

- Do **not** overwrite a file that already exists. If any target file exists, skip it and report it as skipped rather than clobbering the developer's content.
- Only `glossary.md` and `HELMSMAN.md` get starting content. Every other doc MUST be created empty.
- Do not invent additional docs beyond the table above.
