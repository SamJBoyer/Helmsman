---
name: ipool-to-wants
description: Syncs want-like sticky notes from the Lucid iPool into the <wants> section of hDocs/tempPool.md. Resolves the iPool from the <remotes> section of hDocs/master.md via the Lucid MCP server and appends a want only when no similar want already exists in tempPool. Use when pulling iPool stickies into wants, syncing Lucid to tempPool, or when the user invokes iPool-to-wants.
disable-model-invocation: true
---

# iPool to Wants

Pull every want-like sticky from the remote iPool into the `<wants>` section of `hDocs/tempPool.md`, skipping stickies that already have a similar want listed.

iPool: a Lucid document that holds variably-structured thoughts, ideas, questions, and wants. Locate it via the `<remotes>` section of `hDocs/master.md` (`# lucidchart`; see glossary term `iPool`). Remotes is a subsection of master, not a standalone file.

## Scope — do only this

When this skill is invoked, **only** sync iPool stickies → tempPool `<wants>`. Do **not** edit or delete iPool stickies. Do **not** modify other `hDocs/` sections or files (including `<questions>` / `<wonders>` in tempPool), `HELMSMAN.md`, or canon.

## Workflow

```
Task progress:
- [ ] Step 1: Resolve the iPool Lucid document from master.md <remotes>
- [ ] Step 2: Inventory want-like sticky text on the iPool
- [ ] Step 3: Load existing wants from tempPool
- [ ] Step 4: Append wants for stickies that are not already covered
- [ ] Step 5: Report added vs skipped
```

### Step 1: Resolve the iPool

1. Read `hDocs/master.md`.
2. In the `<remotes>` section, find the `<lucidchart>` subsection and the **iPool** connection (name or path containing `iPool`, e.g. `Helmsman-iPool : My Documents/Helmsman/Helmsman-iPool`).
3. If no iPool Lucid entry exists, stop and tell the user to add one under `<remotes>` / `<lucidchart>` in `hDocs/master.md`.
4. Use the **Lucid MCP** server (`search`) with the document title from that entry (e.g. `Helmsman-iPool`) to get the document UUID.
5. If search returns no match or multiple ambiguous matches, stop and ask the user which document to use.

### Step 2: Inventory want-like stickies

Use Lucid MCP against the iPool document id:

1. `fetch` with `metadata_only=true` to learn `page_count` / region layout.
2. Fetch page/region content as needed so you can read **sticky-note text** (and other text areas that clearly express wants).
3. Keep only items that express a desire / outcome to build or change (wants). Skip pure questions, wonders, labels, or unrelated board chrome unless the text is clearly a want.

Build a working set of want texts from the board.

If none are found, stop and report that there is nothing to sync.

### Step 3: Load existing wants from tempPool

Read `hDocs/tempPool.md`. Load wants only from the `<wants>...</wants>` section. Treat each non-empty line as one want. Strip leading list markers/numbers for comparison; keep the listed wording otherwise.

Ignore placeholder lines such as `Initialized as empty.`

If `tempPool.md` is missing, create it with the standard empty sections:

```markdown
<wants>

</wants>
<questions>

</questions>
<wonders>

</wonders>
```

If the file exists but `<wants>` is missing, stop and ask the user before inventing a new section layout.

### Step 4: Append missing wants

For each sticky want from Step 2:

1. **Skip** if a similar want already exists in tempPool `<wants>`.
   - Similar means the same desire / outcome, even if wording differs (paraphrase, shorthand, or partial overlap that clearly targets the same ask).
   - Prefer skipping when unsure whether two wants are the same.
2. **Add** only when no similar want exists:
   - Append a new numbered (or continuing) list item inside `<wants>...</wants>`.
   - Use the sticky text as the want wording (trim only; do not rewrite).
   - Do not reorder or rewrite existing wants.

Do not edit or delete iPool stickies. Do not change `<questions>` or `<wonders>`.

### Step 5: Report

Report:

- iPool document title and id used
- Count added / skipped
- Short list of **added** wants
- Short list of **skipped** wants with the existing tempPool want that matched (brief)

## Constraints

- Use the Lucid MCP server only; do not invent document ids.
- Resolve the source document from `hDocs/master.md` `<remotes>` / `<lucidchart>` iPool entry, then Lucid `search`.
- Never append wants that already have a similar entry in tempPool `<wants>`.
- Only modify `hDocs/tempPool.md` inside `<wants>`; never modify other hDocs, master remotes, or canon.
- Never modify the Lucid iPool as part of this skill.
- If Lucid MCP auth fails, stop and tell the user to re-authenticate the Lucid server.

## Examples

| Situation | Action |
|-----------|--------|
| Sticky: "block agents from reading jot.md"; tempPool already has "hook that denies read access to jot.md" | Skip (same desire) |
| Sticky: "create-question skill"; tempPool wants only mention create-iticket | Append new want |
| No `<lucidchart>` iPool line in master.md `<remotes>` | Stop; ask user to configure remotes |
