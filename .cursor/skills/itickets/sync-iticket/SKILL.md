---
name: sync-iticket
description: Synchronizes open GitHub issues for a given itag with local `.scratch/.itickets/<itag>` markdown files. Downloads missing itickets from GitHub and removes local files for issues no longer open. Use when the user asks to sync itickets, quickssues, ideas, features, or refresh an itag folder under `.scratch/.itickets`.
disable-model-invocation: true
---

# Sync Iticket

Keep `.scratch/.itickets/<itag>` aligned with open GitHub issues labeled `<itag>`.

Shared file format, filename rules, and matching rules: [ITICKET-FORMAT.md](skills/itickets/ITICKET-FORMAT.md).

Valid itags are defined in the `<itag>` section of [glossary.md](../../../docs/glossary.md), the ground truth for which itags exist.

## Parse user input

Extract **itag** from the user's message:

1. Strip optional leading filler: `sync`, `refresh`, `reconcile`.
2. **Itag** — first remaining word (lowercase). Must match a GitHub label and an itag defined in the glossary `<itag>` section.

Examples: `quickssue`, `feature`, `idea`

If no itag can be parsed, ask the user which itag to sync. Do not sync all itags at once unless the user explicitly lists multiple itags.

## Workflow

```
Task progress:
- [ ] Step 1: Parse itag
- [ ] Step 2: List open itickets on GitHub
- [ ] Step 3: Ensure `.scratch/.itickets/<itag>` exists
- [ ] Step 4: Reconcile GitHub → local (add missing files)
- [ ] Step 5: Reconcile local → GitHub (remove stale files)
```

### Step 2: List open itickets on GitHub

Fetch all open issues with the itag label:

```bash
gh issue list --label <itag> --state open --json number,title,body,url
```

If the command fails because the label does not exist, treat GitHub as having zero open itickets for that itag.

### Step 3: Ensure `.scratch/.itickets/<itag>` exists

Create `.scratch/.itickets/<itag>` if it does not exist.

List local iticket files:

```bash
ls .scratch/.itickets/<itag>/*.md
```

If the folder is empty, skip file matching and proceed with GitHub-only reconciliation.

### Step 4: Reconcile GitHub → local

For each open GitHub issue with the itag, check whether a local file already references it using the [matching rule](skills/itickets/ITICKET-FORMAT.md#matching-rule).

For each open issue with no matching local file:

1. Create a new markdown file in `.scratch/.itickets/<itag>`.
2. Use the [filename convention](skills/itickets/ITICKET-FORMAT.md#filename). Avoid collisions by appending the issue number if needed (e.g. `colors-unappealing-1.md`).
3. Use the [iticket template](skills/itickets/ITICKET-FORMAT.md#template). Set `description:` from the issue body (or title if the body is empty). Set `github-issue:` to the issue URL.

### Step 5: Reconcile local → GitHub

For each `.md` file in `.scratch/.itickets/<itag>`:

1. Read its `github-issue:` line.
2. If it references an open GitHub issue from Step 2, keep the file.
3. Otherwise delete the file. This covers closed issues, deleted issues, issues that lost the itag label, and local files with no `github-issue:` line.

## Constraints

- Do **not** create, close, or edit GitHub issues — only read them.
- Do **not** investigate root cause or expand issue scope when creating local files.
- Do **not** modify unrelated files outside `.scratch/.itickets/<itag>`.
- Report a brief summary when done: itag synced, files added, files removed, files unchanged.
