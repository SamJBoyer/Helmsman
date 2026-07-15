---
name: compare-hversions
description: Compares the project's synced docs against the tagged Helmsman canon to detect drift. Use when comparing hVersions, checking canon sync, detecting document drift, or verifying hDocs match a GitHub tag from .helmsman/hVersion.md.
disable-model-invocation: true
---

# Compare hVersions

Detect drift between this hProject's synced documents and the Helmsman canon at the project's tagged hVersion. Ground truth: [canon-lnk/instructions/compare_hVersions.md](canon-lnk/instructions/compare_hVersions.md).

`canon-lnk` is a junction to the Helmsman canon. Read instructions from there; do not read from `canon/` directly.

## Scope — do only this

When this skill is invoked, the agent's job is **only** to compare the tagged canon docs to the project's synced docs and report match vs drift. Do **not** fix drift, edit hDocs, or change `.helmsman/hVersion.md` unless the user explicitly asks.

## Workflow

```
Task progress:
- [ ] Step 1: Read compare_hVersions.md
- [ ] Step 2: Read the hTag from .helmsman/hVersion.md
- [ ] Step 3: Resolve the tagged canon on git
- [ ] Step 4: Compare required c_hDocs to project docs
- [ ] Step 5: Report match or drift
```

### Step 1: Read compare_hVersions.md

Read [canon-lnk/instructions/compare_hVersions.md](canon-lnk/instructions/compare_hVersions.md) and follow it.

### Step 2: Read the hTag

Read `.helmsman/hVersion.md`. Contents should be a git tag (example `v0.0.1`) on the Helmsman GitHub repo.

If the file is missing or empty, stop and report that no hVersion tag is set.

### Step 3: Resolve the tagged canon on git

Checkout (or otherwise load) that tag from git so you can read `canon/c_hDocs` as it existed at the tag.

Prefer reading tagged paths without disrupting the working tree, e.g.:

```bash
git show <htag>:canon/c_hDocs/c_HELMSMAN.md
```

If the tag does not exist locally, fetch tags first. If the tag still cannot be resolved, stop and report the missing tag.

### Step 4: Compare required docs

These `c_*` files **MUST** match the project documents **ad verbatim**. Any mismatch is drift.

| Tagged canon (`canon/c_hDocs/`) | Project path |
|---------------------------------|--------------|
| `c_AGENTS.md` | `AGENTS.md` |
| `c_cursorignore.md` | `.cursorignore` |
| `c_glossary.md` | `hDocs/glossary.md` |
| `c_HELMSMAN.md` | `HELMSMAN.md` |
| `c_master.md` | `hDocs/master.md` |
| `c_overlay.md` | `hDocs/overlay.md` |

Compare each pair byte-for-byte (or exact text). Do **not** treat whitespace-only or “close enough” as a match.

Other hDocs (`artifacts`, `questions`, `status`, `wants`, etc.) are out of scope for this comparison.

### Step 5: Report

For each required pair, report **match** or **drift**.

If every pair matches, report that the project is in sync with hVersion `<htag>`.

If any pair drifts, list the drifted files and state that drift has occurred. Do not auto-fix.

## Constraints

- Always start from [compare_hVersions.md](canon-lnk/instructions/compare_hVersions.md).
- Do **not** edit project docs or canon to “resolve” drift unless the user explicitly asks.
- Do **not** change `.helmsman/hVersion.md` as part of this skill.
- Do **not** invent additional required sync files beyond the table above.
