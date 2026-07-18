---
name: setup-helmsman
description: Scaffold a new Helmsman project by cloning the Helmsman remote at the latest tag and seeding hDocs from canon.
disable-model-invocation: true
---

# Setup Helmsman

Scaffold the Helmsman document structure for a project from the canonical Helmsman repo: https://github.com/SamJBoyer/Helmsman.git

Ground truth for layout: after checkout, read `Helmsman/canon/instructions/init_helmsman.md`.

## Workflow

```
Task progress:
- [ ] Step 1: Clone Helmsman remote, check out the most recent tag, and read init_helmsman.md
- [ ] Step 2: Seed hDocs via seed-hdocs script (deletes the clone)
- [ ] Step 3: Finish remaining init from init_helmsman.md
- [ ] Step 4: Report what was created or skipped
```

### Step 1: Clone Helmsman and check out the latest tag

From the **target project root**:

```bash
git clone https://github.com/SamJBoyer/Helmsman.git Helmsman
cd Helmsman
git fetch --tags
LATEST_TAG=$(git tag -l --sort=-v:refname | head -n 1)
git checkout "$LATEST_TAG"
cd ..
```

PowerShell equivalent:

```powershell
git clone https://github.com/SamJBoyer/Helmsman.git Helmsman
Set-Location Helmsman
git fetch --tags
$LatestTag = (git tag -l --sort=-v:refname | Select-Object -First 1)
git checkout $LatestTag
Set-Location ..
```

If `Helmsman/` already exists, fetch tags and check out the latest tag instead of recloning. Do not overwrite an existing checkout without asking.

**Before seeding**, read `Helmsman/canon/instructions/init_helmsman.md` (the seed script deletes the clone). Record the checked-out tag (e.g. in `.helmsman/hVersion.md` per that file).

### Step 2: Seed hDocs

Run the seed script from the **target project root**. Prefer the script matching the shell:

**PowerShell**

```powershell
& "Skills/setup-helmsman/scripts/seed-hdocs.ps1"
```

**Bash**

```bash
bash Skills/setup-helmsman/scripts/seed-hdocs.sh
```

If this skill lives outside the target repo, pass the absolute path to the script. Optional args: Helmsman dir name (default `Helmsman`), then project root (default cwd).

The script:

1. Copies `Helmsman/canon/c_hDocs/` → `hDocs/` at the project root
2. Moves `hDocs/HELMSMAN.md` → `HELMSMAN.md` at the project root
3. Deletes the `Helmsman/` clone

It refuses to overwrite an existing `hDocs/` or root `HELMSMAN.md`.

### Step 3: Finish remaining init

Using `init_helmsman.md` from Step 1, create any remaining target-structure paths that Step 2 did not produce (e.g. `.helmsman/`, empty docs, `AGENTS.md`). Do **not** overwrite files that already exist.

### Step 4: Report

List every file created and every file skipped because it already existed. Include the Helmsman tag that was checked out.

## Constraints

- Do **not** overwrite a file that already exists. Skip it and report it as skipped.
- Seed content comes only from the tagged `canon/c_hDocs` via the seed script.
- Do not invent additional docs beyond `init_helmsman.md`.
