---
name: wants-to-ipool
description: Syncs wants from the <wants> section of hDocs/tempPool.md onto sticky notes in the Lucid iPool. Resolves the iPool from the <remotes> section of hDocs/master.md via the Lucid MCP server and adds a sticky only when no similar want already exists. Use when pushing wants to the iPool, syncing tempPool wants to Lucid stickies, or when the user invokes wants-to-iPool.
disable-model-invocation: true
---

# Wants to iPool

Push every want in the `<wants>` section of `hDocs/tempPool.md` onto the remote iPool as Lucid sticky notes, skipping wants that already have a similar sticky.

iPool: a Lucid document that holds variably-structured thoughts, ideas, questions, and wants. Locate it via the `<remotes>` section of `hDocs/master.md` (`# lucidchart`; see glossary term `iPool`). Remotes is a subsection of master, not a standalone file.

## Scope — do only this

When this skill is invoked, **only** sync wants → iPool stickies. Do **not** edit `hDocs/`, `HELMSMAN.md`, or other project docs. Do **not** delete or rewrite existing iPool stickies.

## Workflow

```
Task progress:
- [ ] Step 1: Resolve the iPool Lucid document from master.md <remotes>
- [ ] Step 2: Load wants from tempPool
- [ ] Step 3: Inventory existing iPool sticky text
- [ ] Step 4: Add stickies for wants that are not already covered
- [ ] Step 5: Report added vs skipped
```

### Step 1: Resolve the iPool

1. Read `hDocs/master.md`.
2. In the `<remotes>` section, find the `<lucidchart>` subsection and the **iPool** connection (name or path containing `iPool`, e.g. `Helmsman-iPool : My Documents/Helmsman/Helmsman-iPool`).
3. If no iPool Lucid entry exists, stop and tell the user to add one under `<remotes>` / `<lucidchart>` in `hDocs/master.md`.
4. Use the **Lucid MCP** server (`search`) with the document title from that entry (e.g. `Helmsman-iPool`) to get the document UUID.
5. If search returns no match or multiple ambiguous matches, stop and ask the user which document to use.

### Step 2: Load wants from tempPool

Read `hDocs/tempPool.md`. Load wants only from the `<wants>...</wants>` section. Treat each non-empty line as one want (typically a numbered list item). Strip leading list markers/numbers for the sticky text; keep the want wording otherwise.

Ignore placeholder lines such as `Initialized as empty.`

If `tempPool.md` is missing, the `<wants>` section is missing, or there are no real wants, stop and report that there is nothing to sync.

### Step 3: Inventory existing stickies

Use Lucid MCP against the iPool document id:

1. `fetch` with `metadata_only=true` to learn `page_count` / region layout.
2. Fetch page/region content as needed so you can read **existing sticky-note text** (and other text areas that clearly express wants).
3. Optionally use `lucid_search_document` with distinctive phrases from a want when checking for a match — do not treat a substring hit alone as enough if the context is clearly a different idea.

Build a working set of existing want-like texts on the board.

### Step 4: Add missing stickies

For each want from Step 2:

1. **Skip** if a similar want already exists on the iPool.
   - Similar means the same desire / outcome, even if wording differs (paraphrase, shorthand, or partial overlap that clearly targets the same ask).
   - Prefer skipping when unsure whether two wants are the same.
2. **Add** only when no similar sticky exists:
   - Call `lucid_shape_library` / `lucid_shape_details` if needed to confirm the sticky class for this document.
   - Call `lucid_add_block` with `block_type` `StickiesStickyNoteBlock` (or the confirmed sticky class), `document_id` = iPool UUID, and `text` = the want text.
   - Place new stickies in a simple grid so they do not stack on one coordinate (increment `x`/`y` between adds). Do not rearrange existing items.

Do not edit or delete existing sticks. Do not change `tempPool.md`.

### Step 5: Report

Report:

- iPool document title and id used
- Count added / skipped
- Short list of **added** wants
- Short list of **skipped** wants with the existing sticky text that matched (brief)

## Constraints

- Use the Lucid MCP server only; do not invent document ids.
- Resolve the target document from `hDocs/master.md` `<remotes>` / `<lucidchart>` iPool entry, then Lucid `search`.
- Never write stickies for wants that already have a similar sticky on the iPool.
- Never modify `hDocs/` (including `tempPool.md` and `master.md`) as part of this skill.
- Never modify canon.
- If Lucid MCP auth fails, stop and tell the user to re-authenticate the Lucid server.

## Examples

| Situation | Action |
|-----------|--------|
| Want: "hook that denies read access to jot.md"; sticky already says "block agents from reading jot.md" | Skip (same desire) |
| Want: "create-question skill"; stickies only mention create-iticket | Add new sticky |
| No `<lucidchart>` iPool line in master.md `<remotes>` | Stop; ask user to configure remotes |
