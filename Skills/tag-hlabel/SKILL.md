---
name: tag-hlabel
description: Returns the inline emoji for a taken hLabel by name or keyword from hDocs/glossary.md. Use when the user wants to tag, drop, or prefix text with an hLabel emoji, helmsman label marker, or lateral idea tag.
disable-model-invocation: true
---

# Tag hLabel

Look up a **taken** (`[X]`) hLabel and drop its emoji inline. This is the fast inverse of [create-hlabel](../create-hlabel/SKILL.md), which picks an available slot by color.

Ground truth: [glossary.md](../../../hDocs/glossary.md) `# hLabels` section.

## Parse user input

Extract the **label query** from the user's message (text after the skill invocation).
Strip optional leading filler: `tag`, `hlabel`, `label`, `emoji`, `mark`.

Accepted queries:

| Format | Example |
|--------|---------|
| Exact label name | `Ticket-automation` |
| Partial name | `ticket`, `automation` |
| Keyword from usage | `itickets`, `dispatch` |

If no query can be parsed, ask for an hLabel name or keyword.

## Workflow

```
Task progress:
- [ ] Step 1: Parse the label query
- [ ] Step 2: Resolve the taken hLabel
- [ ] Step 3: Drop the emoji inline
```

### Step 1: Parse the label query

Normalize to a single search string. Do not guess across unrelated labels.

### Step 2: Resolve the taken hLabel

Run from the repo root:

```bash
python Skills/tag-hlabel/scripts/tag-hlabel.py "<query>"
```

The script:

- Reads `hDocs/glossary.md` (falls back to `docs/glossary.md`)
- Considers only `[X]` hLabel rows with a defined label name
- Matches by exact name, prefix, substring, or usage keyword
- Prints **only the emoji** on success

If the script exits with code `2`, multiple labels tied — ask the user to be more specific.
If no match, say no taken hLabel matches and stop. Do **not** invent emojis.

For debugging only:

```bash
python Skills/tag-hlabel/scripts/tag-hlabel.py "<query>" --verbose
```

### Step 3: Drop the emoji inline

**Default output:** reply with **only the emoji** — no preamble, no explanation.

When the user also provided text to tag, prefix that text with the emoji and a single space:

```text
🔴 ticket ingestion should run on push
```

When tagging an existing file or selection, insert the emoji immediately before the matched term or at the start of the line — minimal edit, no other changes.

Do **not** edit `hDocs/glossary.md` unless the user explicitly asks to claim or change an hLabel.

## Constraints

- Only match against **taken** (`[X]`) hLabels with a real label name.
- Do **not** use available (`[ ]`) palette slots — use `create-hlabel` for those.
- Do **not** add terms or modify glossary definitions without explicit permission.
- Keep responses short; this skill is for quick inline markers.

## Examples

| Input | Output |
|-------|--------|
| `Ticket-automation` | `🔴` |
| `tag ticket automation` | `🔴` |
| `tag ticket colors look washed` | `🔴 colors look washed` |
