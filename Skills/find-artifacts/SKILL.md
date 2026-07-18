---
name: find-artifacts
description: Scans the codebase for vestigial features, code, and names that do not match ongoing efforts in the Lucid iPool (and related hDocs), optionally confirms via git history, then proposes a summary for the <artifacts> section of hDocs/master.md. Use when hunting dead code, abandoned names, leftover features, workspace dirt from prior attempts, or when the user invokes find-artifacts.
disable-model-invocation: true
---

# Find Artifacts

Find vestigial features, code, and names in the repo that look unrelated to ongoing efforts, compare them against the iPool, optionally confirm with git history, then **propose** a summary for `hDocs/master.md` `<artifacts>`.

**Artifact** (Helmsman): work, features, or content from abandoned attempts that may dirty the workspace. The artifacts log explains weird behavior or odd architectural choices before you dig git history. See HELMSMAN.md `<master>` / artifacts.

## Scope — do only this

When this skill is invoked:

1. Inventory ongoing efforts (iPool + supporting hDocs).
2. Scan the codebase for vestigial candidates.
3. Optionally use git history to confirm abandonment / prior-effort lineage.
4. **Propose** a summary for `hDocs/master.md` `<artifacts>`.

Do **not** delete code, rename symbols, or “clean up” candidates. Do **not** edit `hDocs/` (including `master.md`) or canon until the user **explicitly** approves writing the proposal. Do **not** modify the Lucid iPool.

## Workflow

```
Task progress:
- [ ] Step 1: Resolve ongoing efforts (iPool + hDocs)
- [ ] Step 2: Scan code for vestigial candidates
- [ ] Step 3: Cross-check candidates against ongoing efforts
- [ ] Step 4: Confirm with git history when useful
- [ ] Step 5: Propose summary for master.md <artifacts>
- [ ] Step 6: Write only if the user explicitly approves
```

### Step 1: Resolve ongoing efforts

Build a working set of **current purpose** signals:

1. **iPool (required)**  
   - Read `hDocs/master.md`. In `<remotes>`, find the `<lucidchart>` iPool entry (name/path containing `iPool`).  
   - Legacy layout: if `<remotes>` is missing from `master.md` but `hDocs/remotes.md` exists, use that file the same way.  
   - If no iPool entry exists, stop and ask the user to configure remotes.  
   - Use Lucid MCP `search` with the document title to get the UUID. On ambiguous/no match, ask the user.  
   - Fetch sticky / text content (metadata first, then pages/regions as needed). Prefer want-like and feature-like ideas; skip board chrome.

2. **Supporting docs (read only)**  
   - Glossary terms (`hDocs/glossary.md` or terms section if nested in master).  
   - Wants / tempPool (`hDocs/tempPool.md` `<wants>`, or legacy `hDocs/wants.md`).  
   - Existing artifacts log: `hDocs/master.md` `<artifacts>`, and if present `hDocs/artifacts.md` (legacy split).  
   - Drift / status if present (`<drift>` in master, or `hDocs/status.md`).

Ongoing effort = anything clearly represented in the iPool or those supporting docs.

### Step 2: Scan for vestigial candidates

Search the codebase (and project Skills) for:

- Features, modules, flags, scripts, or paths with **no clear tie** to ongoing efforts
- Names / terms that look **orphaned** (not in glossary, not in iPool/wants, not used by current workflows)
- Dead references, abandoned branch leftovers, or “previous attempt” scaffolding that still sits in tree
- Anything that **does not make sense** relative to current Helmsman purpose

Be explicit and skeptical: prefer false negatives over flooding the log. Skip generated deps (`node_modules`, build output, `.scratch`, etc.) unless the user asks to include them.

### Step 3: Cross-check against ongoing efforts

For each candidate, classify:

| Label | Meaning |
|-------|---------|
| **Likely artifact** | No meaningful link to iPool / wants / glossary / drift priorities |
| **Uncertain** | Weak or ambiguous link — need history or user judgment |
| **Active** | Clearly supports an ongoing effort — do not propose as artifact |

Similar intent counts as a link even when wording differs (same desire/outcome). Prefer **Uncertain** when unsure.

### Step 4: Git history (when useful)

Use git to strengthen or dismiss candidates — especially **Uncertain** ones:

- `git log` / `git log -S` / `git log -G` on paths or distinctive names
- Blame or commit messages that show a prior initiative that never landed in current iPool
- Branch / path history that marks something as abandoned

Do not dump full history. For each confirmed artifact, note a **short** lineage (e.g. last meaningful commit hash + one-line why it looks abandoned).

Respect any existing artifacts notes (e.g. commit cutoffs already recorded in `<artifacts>` or `artifacts.md`).

### Step 5: Propose summary for `master.md` `<artifacts>`

Present a **proposal** in chat — do not write files yet. Use this shape:

```markdown
## Artifact findings (proposal)

### Confirmed / likely
- **<name or path>**: <why vestigial> | iPool link: none | git: <optional short evidence>

### Uncertain (needs your call)
- **<name or path>**: <why unclear> | possible link: <if any> | git: <optional>

### Already logged (no change)
- <existing entry that still applies>
```

Then show the **exact text** you would place (or append) inside `hDocs/master.md` `<artifacts>...</artifacts>`:

- Append new findings; do not silently delete existing entries.
- Keep entries concise: what it is, why it is an artifact, optional commit/path pointer.
- If `master.md` has no `<artifacts>` block yet, propose adding one (canon shape). If legacy `hDocs/artifacts.md` holds the only log, propose migrating/merging into `master.md` `<artifacts>` and say so clearly — still wait for approval before editing.

### Step 6: Write only with explicit approval

If the user approves writing:

1. Update **only** `hDocs/master.md` inside `<artifacts>...</artifacts>` (create the section if approved).
2. Do not edit canon, Lucid, or unrelated hDocs sections.
3. Report what was written vs left as uncertain.

If the user declines or only wanted the report, stop after Step 5.

## Constraints

- Compare code to the **iPool** as the primary “ongoing efforts” source; hDocs are secondary signals.
- Search **explicitly** for vestigial features, code, and names unrelated to ongoing efforts.
- Use git history to uncover prior-effort lineage — not as a substitute for reading the iPool.
- **Propose** the summary for `master.md` `#artifacts` / `<artifacts>`; never write hDocs without explicit permission.
- Never modify canon.
- If Lucid MCP auth fails, stop and tell the user to re-authenticate the Lucid server.

## Examples

| Situation | Action |
|-----------|--------|
| Script `tag-hlabel.py` exists; iPool/wants never mention it; last commit was a abandoned experiment | Likely artifact → propose for `<artifacts>` |
| Skill name matches an iPool sticky want | Active → do not propose |
| Odd folder name; git shows it belonged to a pre-cutoff branch already noted in artifacts | Already logged → mention under “no change” unless new detail is useful |
| No iPool remotes entry | Stop; ask user to configure `<remotes>` / `<lucidchart>` |
