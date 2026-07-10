---
name: create-hlabel
description: Finds the closest available hLabel emoji for a given color using the hLabels palette in docs/glossary.md. Use when the user wants to pick, assign, or match an hLabel, helmsman label, colored emoji label, or needs the nearest palette slot for a hex/RGB/named color.
disable-model-invocation: true
---

# Create hLabel

Match an input color to the nearest **available** hLabel in the glossary. Available slots
are lines marked `[ ]`; taken slots (`[X]`) are ignored.

Ground truth: [glossary.md](../../../docs/glossary.md) `# hLabels` section.

## Parse user input

Extract the target **color** from the user's message (text after the skill invocation).
Strip optional leading filler: `hlabel`, `label`, `match`, `find`.

Accepted color formats:

| Format | Example |
|--------|---------|
| Hex | `#EA4335`, `EA4335` |
| RGB | `rgb(234, 67, 53)` |
| Basic name | `red`, `orange`, `blue`, `white` |

If no color can be parsed, ask the user for one.

## Workflow

```
Task progress:
- [ ] Step 1: Parse the target color
- [ ] Step 2: Find the closest available hLabel
- [ ] Step 3: Report the match
```

### Step 1: Parse the target color

Normalize the color to RGB. If the format is unsupported, ask the user to provide hex,
RGB, or a basic color name.

### Step 2: Find the closest available hLabel

Run from the repo root:

```bash
python Skillet/create-hlabel/scripts/find-hlabel.py "<color>"
```

The script:

- Reads `docs/glossary.md`
- Considers only `[ ]` hLabel rows
- Computes Euclidean RGB distance to each available slot
- Returns the closest match(es); ties share the same distance

If the script reports no available hLabels, stop and tell the user every slot is taken.

### Step 3: Report the match

Report:

- Input color (as RGB)
- Closest available hLabel emoji and hex
- Distance (lower is closer)
- The exact glossary line format to claim it, with placeholders left for the user:

```text
[X]: <emoji> <hex>, [label], [useage]
```

Do **not** edit `docs/glossary.md` unless the user explicitly asks to claim the hLabel.

## Constraints

- Only match against **available** (`[ ]`) hLabels.
- Do **not** add terms or modify glossary definitions without explicit permission.
- Do **not** invent new palette colors outside the glossary hLabels section.
- If multiple emoji slots share the same hex and distance, list all tied matches.

## Examples

| Input | Closest available |
|-------|-------------------|
| `#EA4335` | `🔴 #EA4335` (distance 0) |
| `#FF0000` | `🔴 #EA4335` or `🟥 #EA4335` (nearest red slot) |
| `rgb(60, 120, 200)` | `🔵 #4285F4` or `🟦 #4285F4` (nearest blue slot) |
