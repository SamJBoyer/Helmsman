---
name: setup-helmsman
description: Scaffold a new Helmsman project by following a helmsman setup from a canonical helmsman version. 
disable-model-invocation: true
---

# Setup Helmsman

Scaffold the Helmsman document structure for a project. Ground truth: [canon-lnk/instructions/init_helmsman.md](canon-lnk/instructions/init_helmsman.md).

`canon-lnk` is a junction to the Helmsman canon. Read and copy seeded docs from there; do not read from `canon/` directly.

## Workflow

```
Task progress:
- [ ] Step 1: Read init_helmsman.md and execute instructions in the new repo to create the repo structure
- [ ] Step 2: Copy seeded docs from canon-lnk
- [ ] Step 3: Create the remaining docs as empty files
- [ ] Step 4: Report what was created or skipped
```

### Step 1: Read init_helmsman.md

Read [canon-lnk/instructions/init_helmsman.md](canon-lnk/instructions/init_helmsman.md) for the directory layout and which files get content vs stay empty. Create the document structure as outlined
in init_helmsman.md

### Step 2: Copy seeded docs from canon-lnk

Copy these **verbatim** from [canon-lnk/c_hDocs/](canon-lnk/c_hDocs/):

| Canon source | Destination |
|--------------|-------------|
| `c_glossary.md` | `hDocs/glossary.md` |
| `c_master.md` | `hDocs/master.md` |
| `c_HELMSMAN.md` | `HELMSMAN.md` (repo root) |
| `c_AGENTS.md` | `AGENTS.md` (repo root) |

### Step 3: Create empty docs

Create `hDocs/` if needed, then create these as **empty** files:

- `hDocs/artifacts.md`
- `hDocs/overlay.md`
- `hDocs/questions.md`
- `hDocs/status.md`
- `hDocs/wants.md`

### Step 4: Report

List every file created and every file skipped because it already existed.

## Constraints

- Do **not** overwrite a file that already exists. Skip it and report it as skipped.
- Only the seeded files above get starting content. Every other doc MUST be created empty.
- Do not invent additional docs beyond [init_helmsman.md](canon-lnk/instructions/init_helmsman.md).
