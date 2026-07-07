---
name: create-iticket
description: Briefly summarizes an issue, saves it locally under a tag-specific folder, and creates a GitHub issue with that label. Use when the user wants to create an iticket, quickssue, idea, feature, or any tagged git issue from casual input without deep investigation.
disable-model-invocation: true
---

# Create Iticket

Quickly record a tagged issue without deep inquiry about its origin or implications.

Shared file format, filename rules, and label setup: [ITICKET-FORMAT.md](skills/itickets/ITICKET-FORMAT.md).

## Parse user input

Extract **tag** and **summary** from the user's message (text after the skill invocation):

1. Strip optional leading filler: `new`, `a`, `an`, `create`, `add`.
2. **Tag** — first remaining word (lowercase). Becomes the GitHub label and local subfolder.
3. **Summary** — everything after the tag. Used for `description`, filename, and issue title/body.

| Input | Tag | Summary |
|-------|-----|---------|
| `new quickssue colors look bad` | `quickssue` | `colors look bad` |
| `feature dark mode toggle` | `feature` | `dark mode toggle` |
| `idea cache search results` | `idea` | `cache search results` |

If no tag or summary can be parsed, ask the user for both. Do not guess.

## Workflow

```
Task progress:
- [ ] Step 1: Parse tag and summary
- [ ] Step 2: Draft the iticket file
- [ ] Step 3: Create the GitHub issue
- [ ] Step 4: Link the issue back to the file
```

### Step 2: Draft the iticket file

In `.scratch/.itickets/<tag>`, create a new markdown file using the [iticket template](skills/itickets/ITICKET-FORMAT.md#template). Fill in `description:` only for now. Perform minor summarization on the summary text, plus minor grammar or spelling corrections.

Use the [filename convention](skills/itickets/ITICKET-FORMAT.md#filename): three lowercase words joined by hyphens (e.g. `colors-look-bad.md`).

Create `.scratch/.itickets/<tag>` if it does not exist.

### Step 3: Create the GitHub issue

After writing the document, create a GitHub issue with the `<tag>` label:

```bash
gh issue create --title "<issue title>" --body "<issue body>" --label <tag>
```

- **Title:** short, derived from the summary (can match the 3-word filename theme).
- **Body:** the polished `description` from the iticket file. Keep it brief — do not expand scope or add acceptance criteria unless the user provided them.
- If the label does not exist, create it first (see [GitHub label](skills/itickets/ITICKET-FORMAT.md#github-label)).

### Step 4: Link the issue back to the file

Add the `github-issue:` line to the iticket file per the [template](skills/itickets/ITICKET-FORMAT.md#template). Use the issue number or URL.

## Constraints

- Do **not** investigate root cause, explore the codebase, or ask clarifying questions unless the user's input is completely unintelligible.
- Do **not** turn this into a full triage or vertical-slice breakdown; use `to-issues` for that.
- Do **not** close or modify unrelated issues.
