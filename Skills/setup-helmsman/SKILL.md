---
name: setup-helmsman
description: Scaffold a new Helmsman project by creating the standard .helmsman/, hDocs/, HELMSMAN.md, and AGENTS.md structure. Seeded docs are copied from template-link. Use when the user asks to set up Helmsman, scaffold Helmsman docs, or initialize a new Helmsman project.
disable-model-invocation: true
---

# Setup Helmsman

Scaffold the Helmsman document structure for a project. Ground truth: [template-link/init_helmsman.md](template-link/init_helmsman.md).

## Workflow

```
Task progress:
- [ ] Step 1: Read init_helmsman.md
- [ ] Step 2: Create .helmsman/.chronology/ and empty .helmsman/version.md
- [ ] Step 3: Copy seeded docs from template-link
- [ ] Step 4: Create the remaining docs as empty files
- [ ] Step 5: Report what was created or skipped
```

### Step 1: Read init_helmsman.md

Read [template-link/init_helmsman.md](template-link/init_helmsman.md) for the directory layout and which files get content vs stay empty.

### Step 2: Create .helmsman/

Create `.helmsman/.chronology/` and an empty `.helmsman/version.md`.

### Step 3: Copy seeded docs from template-link

Copy these **verbatim** from [template-link/](template-link/):

| Template | Destination |
|----------|-------------|
| `glossary.md` | `hDocs/glossary.md` |
| `master.md` | `hDocs/master.md` |
| `HELMSMAN.md` | `HELMSMAN.md` (repo root) |

Copy `AGENTS.md` verbatim from `canon/helmsman_docs/AGENTS.md` to the repo root. It is not in template-link but is required by init_helmsman.

### Step 4: Create empty docs

Create `hDocs/` if needed, then create these as **empty** files:

- `hDocs/artifacts.md`
- `hDocs/jot.md`
- `hDocs/overlay.md`
- `hDocs/questions.md`
- `hDocs/status.md`
- `hDocs/wants.md`

### Step 5: Report

List every file created and every file skipped because it already existed.

## Constraints

- Do **not** overwrite a file that already exists. Skip it and report it as skipped.
- Only the seeded files above get starting content. Every other doc MUST be created empty.
- Do not invent additional docs beyond [init_helmsman.md](template-link/init_helmsman.md).
