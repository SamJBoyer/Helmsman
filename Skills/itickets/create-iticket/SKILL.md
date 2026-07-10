---
name: create-iticket
description: Records an itagged issue locally and on GitHub. Use when the user wants to create an iticket, quickssue, idea, feature, or any itagged git issue from casual input. The agent only validates the summary, ensures the itag exists, and files the issue — never implements the ticket.
disable-model-invocation: true
---

# Create Iticket

Record an itagged issue on GitHub and in `.scratch/.itickets/`. Every iticket MUST have exactly one itag.

## Scope — do only this

When this skill is invoked, the agent's job is **only** to prepare the itag and push the iticket. Do **not** do anything else.

1. **Check coherence** — confirm the summary is a coherent sentence (minor grammar/spelling fixes only). If the input is unintelligible, ask the user to rephrase. Do not investigate, explore, or expand.
2. **Check the itag** — confirm the itag exists in the glossary `<itag>` section and as a GitHub label.
3. **Create the itag if missing** — if the itag is not in the glossary, add a minimal entry to the `<itag>` section. If the GitHub label does not exist, create it (see [GitHub label](../ITICKET-FORMAT.md#github-label)).
4. **Push the iticket** — write the local iticket file and create the GitHub issue with that itag as its label.

**Never implement the ticket.** Do not write code, edit project files, explore the codebase, pool the iticket, triage scope, add acceptance criteria, or start work on what the issue describes. Filing the issue is the entire task.

Shared file format, filename rules, and label setup: [ITICKET-FORMAT.md](../ITICKET-FORMAT.md).

Valid itags and their meanings are defined in the `<itag>` section of [glossary.md](../../../docs/glossary.md).

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

**Coherence check.** The summary must read as a coherent sentence after light editing. If it does not, stop and ask the user to rephrase — do not guess intent or fill in missing context.

**Ensure the itag exists.** Check the glossary `<itag>` section and GitHub labels. If the itag is missing from the glossary, add a minimal entry (itag name plus a one-line description derived from context or the itag name). If the GitHub label is missing, create it before opening the issue.

## Workflow

```
Task progress:
- [ ] Step 1: Parse input, check coherence, and ensure itag exists
- [ ] Step 2: Draft the iticket file
- [ ] Step 3: Create the GitHub issue
- [ ] Step 4: Link the issue back to the file
- [ ] Step 5: Revise the source document (only if the revise flag is set)
```

### Step 2: Draft the iticket file

In `.scratch/.itickets/<itag>`, create a new markdown file using the [iticket template](../ITICKET-FORMAT.md#template). Fill in `description:` only for now. Apply minor grammar or spelling corrections so the summary is a coherent sentence — do not expand scope or add detail the user did not provide.

Use the [filename convention](../ITICKET-FORMAT.md#filename): three lowercase words joined by hyphens (e.g. `colors-look-bad.md`).

Create `.scratch/.itickets/<itag>` if it does not exist.

### Step 3: Create the GitHub issue

After writing the document, create a GitHub issue with the `<itag>` label:

```bash
gh issue create --title "<issue title>" --body "<issue body>" --label <itag>
```

- **Title:** short, derived from the summary (can match the 3-word filename theme).
- **Body:** the polished `description` from the iticket file. Keep it brief — do not expand scope or add acceptance criteria unless the user provided them.
- If the label does not exist, create it first (see [GitHub label](../ITICKET-FORMAT.md#github-label)).

### Step 4: Link the issue back to the file

Add the `github-issue:` line to the iticket file per the [template](../ITICKET-FORMAT.md#template). Use the issue number or URL.

### Step 5: Revise the source document

Only run this step when the revise flag is set (the user included `revise`) **and** the summary text was copied from `docs/wants.md` or `docs/questions.md`.

Delete the copied text from its source file, since the iticket now supersedes it. Remove only the specific line(s) or entry that was copied — do not touch unrelated content, and do not renumber or reformat the rest of the file. If you cannot confidently identify the source text in `docs/wants.md` or `docs/questions.md`, skip this step and report that the source was not revised.

## Constraints

- Every iticket MUST have exactly one itag. Never create an iticket without one.
- **Never implement the ticket.** Do not write code, modify project source, run builds, pool the iticket, or take any action beyond filing the issue.
- Do **not** investigate root cause, explore the codebase, or ask clarifying questions except when the summary is not a coherent sentence or the itag/summary cannot be parsed.
- Do **not** turn this into a full triage or vertical-slice breakdown; use `to-issues` for that.
- Do **not** close or modify unrelated issues.
