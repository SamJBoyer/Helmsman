---
name: check-canon-drift
description: Clones Helmsman into .scratch at the latest tag (or the tag in .helmsman/hVersion.md for an hProject) and compares the project's HELMSMAN.md to the tagged canon. Use when checking HELMSMAN.md canon drift, verifying Helmsman sync, or when the user invokes check-canon-drift.
disable-model-invocation: true
---

# Check Canon Drift

Detect drift between this project's root `HELMSMAN.md` and the Helmsman canon `HELMSMAN.md` at a resolved git tag.

Remote: https://github.com/SamJBoyer/Helmsman.git

## Scope — do only this

When this skill is invoked, **only** resolve the tag, clone/checkout into `.scratch`, compare `HELMSMAN.md`, and report match vs drift. Do **not** fix drift, edit `HELMSMAN.md`, edit canon, or change `.helmsman/hVersion.md` unless the user explicitly asks.

## Workflow

```
Task progress:
- [ ] Step 1: Resolve the Helmsman tag
- [ ] Step 2: Clone or update Helmsman under .scratch
- [ ] Step 3: Compare HELMSMAN.md to canon
- [ ] Step 4: Report match or drift
```

### Step 1: Resolve the Helmsman tag

From the **project root**:

1. If `.helmsman/hVersion.md` exists and contains a non-empty tag (e.g. `v0.0.1`), this project is an **hProject**. Use that tag as `TAG`.
2. Otherwise, use the **latest** version tag from the Helmsman remote as `TAG`.

Trim whitespace from `hVersion.md`; the file should be only the tag string.

### Step 2: Clone or update Helmsman under `.scratch`

Checkout lives at `.scratch/Helmsman` (`.scratch/` is gitignored).

**Bash**

```bash
mkdir -p .scratch
if [ ! -d .scratch/Helmsman/.git ]; then
  git clone https://github.com/SamJBoyer/Helmsman.git .scratch/Helmsman
fi
cd .scratch/Helmsman
git fetch --tags
# If TAG was not set from hVersion.md:
# TAG=$(git tag -l --sort=-v:refname | head -n 1)
git checkout "$TAG"
cd ../..
```

**PowerShell**

```powershell
New-Item -ItemType Directory -Force -Path .scratch | Out-Null
if (-not (Test-Path .scratch/Helmsman/.git)) {
  git clone https://github.com/SamJBoyer/Helmsman.git .scratch/Helmsman
}
Set-Location .scratch/Helmsman
git fetch --tags
# If TAG was not set from hVersion.md:
# $TAG = (git tag -l --sort=-v:refname | Select-Object -First 1)
git checkout $TAG
Set-Location ../..
```

If `.scratch/Helmsman` already exists, fetch tags and check out `TAG` — do not delete and reclone unless the checkout is broken.

If `TAG` cannot be resolved after fetch, stop and report the missing tag.

### Step 3: Compare HELMSMAN.md to canon

| Project path | Canon path (under `.scratch/Helmsman/`) |
|--------------|------------------------------------------|
| `HELMSMAN.md` | `canon/c_hDocs/HELMSMAN.md` |

Compare byte-for-byte (or exact text). Whitespace-only or “close enough” is still **drift**.

If the project root has no `HELMSMAN.md`, stop and report that there is nothing to compare.

If the canon file is missing at that tag, stop and report the missing path.

### Step 4: Report

Report:

- Which `TAG` was used and why (hVersion vs latest)
- **match** or **drift** for `HELMSMAN.md`

If they match, state the project `HELMSMAN.md` is in sync with Helmsman canon at `TAG`.

If they drift, state that drift has occurred. Do not auto-fix. Optionally summarize what differs (e.g. `diff` hunks) if useful — keep it brief.

## Constraints

- Clone only under `.scratch/Helmsman`.
- Do **not** edit project docs, canon, or `.helmsman/hVersion.md` to “resolve” drift unless the user explicitly asks.
- Do **not** compare other hDocs or AGENTS files — this skill is `HELMSMAN.md` only.
- Prefer reusing an existing `.scratch/Helmsman` checkout over recloning.
