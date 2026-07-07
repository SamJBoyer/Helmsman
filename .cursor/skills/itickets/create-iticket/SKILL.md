---
name: create-iticket
description: Briefly summarizes an issue, saves it locally under an itag-specific folder, and creates a GitHub issue with that itag as its label. Use when the user wants to create an iticket, quickssue, idea, feature, or any itagged git issue from casual input without deep investigation.
disable-model-invocation: true
---

# Create Iticket

Quickly record an itagged issue without deep inquiry about its origin or implications. Every iticket MUST have exactly one itag.

Shared file format, filename rules, and label setup: [ITICKET-FORMAT.md](skills/itickets/ITICKET-FORMAT.md).

Valid itags and their meanings are defined in the `<itag>` section of [glossary.md](../../../docs/glossary.md), which is the ground truth for which itags exist and when to use each one.

## Parse user input

Extract **itag** and **summary** from the user's message (text after the skill invocation):

1. Strip optional leading filler: `new`, `a`, `an`, `create`, `add`.
2. **Itag** — first remaining word (lowercase). Becomes the GitHub label and local subfolder.
3. **Summary** — everything after the itag. Used for `description`, filename, and issue title/body.

| Input | Itag | Summary |
|-------|-----|---------|
| `new quickssue colors look bad` | `quickssue` | `colors look bad` |
| `feature dark mode toggle` | `feature` | `dark mode toggle` |
| `idea cache search results` | `idea` | `cache search results` |

**Revise flag.** If the input contains the word `revise`, remove it before extracting the itag and summary, and set the revise flag. When the flag is set and the summary text was copied from `docs/wants.md` or `docs/questions.md`, delete that source text from the file after the iticket is created (see Step 5).

If no itag or summary can be parsed, ask the user for both. Do not guess.

**Validate the itag.** The itag MUST be one of the itags defined in the `<itag>` section of [glossary.md](../../../docs/glossary.md). If the parsed itag is not defined there, stop and ask the user to pick a valid itag (or to confirm adding a new itag to the glossary first). Never create an iticket without a valid itag.

## Workflow

```
Task progress:
- [ ] Step 1: Parse and validate itag and summary
- [ ] Step 2: Draft the iticket file
- [ ] Step 3: Create the GitHub issue
- [ ] Step 4: Link the issue back to the file
- [ ] Step 5: Revise the source document (only if the revise flag is set)
```

### Step 2: Draft the iticket file

In `.scratch/.itickets/<itag>`, create a new markdown file using the [iticket template](skills/itickets/ITICKET-FORMAT.md#template). Fill in `description:` only for now. Perform minor summarization on the summary text, plus minor grammar or spelling corrections.

Use the [filename convention](skills/itickets/ITICKET-FORMAT.md#filename): three lowercase words joined by hyphens (e.g. `colors-look-bad.md`).

Create `.scratch/.itickets/<itag>` if it does not exist.

### Step 3: Create the GitHub issue

After writing the document, create a GitHub issue with the `<itag>` label:

```bash
gh issue create --title "<issue title>" --body "<issue body>" --label <itag>
```

- **Title:** short, derived from the summary (can match the 3-word filename theme).
- **Body:** the polished `description` from the iticket file. Keep it brief — do not expand scope or add acceptance criteria unless the user provided them.
- If the label does not exist, create it first (see [GitHub label](skills/itickets/ITICKET-FORMAT.md#github-label)).

### Step 4: Link the issue back to the file

Add the `github-issue:` line to the iticket file per the [template](skills/itickets/ITICKET-FORMAT.md#template). Use the issue number or URL.

### Step 5: Revise the source document

Only run this step when the revise flag is set (the user included `revise`) **and** the summary text was copied from `docs/wants.md` or `docs/questions.md`.

Delete the copied text from its source file, since the iticket now supersedes it. Remove only the specific line(s) or entry that was copied — do not touch unrelated content, and do not renumber or reformat the rest of the file. If you cannot confidently identify the source text in `docs/wants.md` or `docs/questions.md`, skip this step and report that the source was not revised.

## Constraints

- Every iticket MUST have exactly one valid itag from the glossary `<itag>` section. Never create an iticket without one.
- Do **not** investigate root cause, explore the codebase, or ask clarifying questions unless the user's input is completely unintelligible (the itag is the one thing you must always confirm).
- Do **not** turn this into a full triage or vertical-slice breakdown; use `to-issues` for that.
- Do **not** close or modify unrelated issues.
