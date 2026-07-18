---
name: check-doc-drift
description: >-
  Audits implemented and tested features in the repo, compares them to
  hDocs/master.md summary, and proposes an update to master.md drift.
  Use when the user invokes check-doc-drift, asks for doc drift, summary vs
  code drift, or whether docs outpace (or lag) the codebase.
disable-model-invocation: true
---

# Check Doc Drift

Bridge aspirational docs and code reality: inventory what is implemented (and tested), compare that to `hDocs/master.md` `<summary>`, then **propose** (do not apply) a `<drift>` update.

This is **not** canon sync. For HELMSMAN.md vs tagged canon, use `check-canon-drift`. For multi-file hVersion sync, use `compare-hVersions`.

## Scope — do only this

1. Inventory the codebase for implemented features and tests.
2. Read `hDocs/master.md` `<summary>` (and existing `<drift>` if present).
3. Diff aspiration vs reality in both directions.
4. Propose replacement text for `hDocs/master.md` `<drift>`.

Do **not** edit `hDocs/`, canon, or other docs unless the user explicitly asks to apply the proposal. Never modify canon without asking.

## Workflow

```
Task progress:
- [ ] Step 1: Read summary and related hDocs context
- [ ] Step 2: Inventory implemented features
- [ ] Step 3: Inventory tests / verification
- [ ] Step 4: Compare both directions
- [ ] Step 5: Propose master.md <drift>
```

### Step 1: Read summary and related hDocs context

From project root, read:

- `hDocs/master.md` — especially `<summary>` and any existing `<drift>`
- Skim for claims: `hDocs/status.md`, `hDocs/wants.md`, `hDocs/overlay.md`, `HELMSMAN.md`, `hDocs/glossary.md`

Treat `<summary>` as the aspirational “what this project is.” Other hDocs inform judgment but the primary comparison target is `<summary>`.

### Step 2: Inventory implemented features

Pay special attention to what actually exists and is usable **now** (working tree, not only git history):

| Area | Where to look |
|------|----------------|
| Agent skills | `Skills/**/SKILL.md` |
| Scripts / tooling | `Skills/**/scripts/`, other executables |
| Canon / versioning | `canon/`, `.helmsman/hVersion.md`, `canon/tag.md` |
| Feature pool | `fPool/` |
| Hooks / enforcement | hooks configs, `.cursor/`, deny/write policies |
| Remotes / integrations | Lucid/MCP usage described by skills, `hDocs/remotes.md` |

For each notable capability, note: **present on disk**, **broken/partial**, or **deleted in working tree but still in git**.

### Step 3: Inventory tests / verification

Search for automated tests and CI (e.g. `test/`, `*_test*`, `*.spec.*`, `.github/workflows`, package test scripts).

If none exist, say so explicitly — “implemented” without tests is still implemented, but drift should not claim coverage that is not there.

Manual skill procedures and prose rules in `HELMSMAN.md` / `AGENTS.md` are **not** tests.

### Step 4: Compare both directions

Build two lists:

**A. Docs ahead of code** — features or capabilities implied by `<summary>` (or clearly presented as current project purpose in related docs the summary rests on) that are **not** implemented, only stubbed, deleted on disk, or untested where the summary implies a working system.

**B. Code ahead of docs** — implemented skills, scripts, pools, or tooling that are **not** represented in `<summary>`.

Be concrete (name skills/paths). Prefer current working-tree truth over abandoned branches; use `hDocs/artifacts.md` if weird leftovers appear.

### Step 5: Propose `master.md` `<drift>`

Output a ready-to-paste proposal for the `<drift>` section. Do not write the file unless asked.

Use this shape (match existing XML-ish section style in `master.md`):

```markdown
<drift>

[1–3 sentences: overall verdict — docs ahead, code ahead, or mixed.]

Docs ahead of code:
- ...

Code ahead of docs:
- ...

Tests: [none | brief note of what exists]

</drift>
```

If a list side is empty, write `None.` for that side.

Also briefly state whether applying this would replace or create `<drift>` (current `master.md` may lack the section).

## Constraints

- Propose only; never edit `hDocs` without explicit permission.
- Never modify canon without asking.
- Do not run `check-canon-drift` / `compare-hVersions` unless the user also asked for those.
- Do not invent features; ground every bullet in a path or missing path.
- Keep the proposed `<drift>` concise enough for a human to skim — not a full repo dump.
