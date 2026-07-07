---
name: sync-iticket
description: Synchronizes open GitHub issues for a given tag with local `.scratch/.itickets/<tag>` markdown files. Downloads missing itickets from GitHub and removes local files for issues no longer open. Use when the user asks to sync itickets, quickssues, ideas, features, or refresh a tag folder under `.scratch/.itickets`.
disable-model-invocation: true
---

# Sync Iticket

Keep `.scratch/.itickets/<tag>` aligned with open GitHub issues labeled `<tag>`.

Shared file format, filename rules, and matching rules: [ITICKET-FORMAT.md](skills/itickets/ITICKET-FORMAT.md).

## Parse user input

Extract **tag** from the user's message:

1. Strip optional leading filler: `sync`, `refresh`, `reconcile`.
2. **Tag** — first remaining word (lowercase). Must match a GitHub label.

Examples: `quickssue`, `feature`, `idea`

If no tag can be parsed, ask the user which tag to sync. Do not sync all tags at once unless the user explicitly lists multiple tags.

## Workflow

```
Task progress:
- [ ] Step 1: Parse tag
- [ ] Step 2: List open itickets on GitHub
- [ ] Step 3: Ensure `.scratch/.itickets/<tag>` exists
- [ ] Step 4: Reconcile GitHub → local (add missing files)
- [ ] Step 5: Reconcile local → GitHub (remove stale files)
```

### Step 2: List open itickets on GitHub

Fetch all open issues with the tag label:

```bash
gh issue list --label <tag> --state open --json number,title,body,url
```

If the command fails because the label does not exist, treat GitHub as having zero open itickets for that tag.

### Step 3: Ensure `.scratch/.itickets/<tag>` exists

Create `.scratch/.itickets/<tag>` if it does not exist.

List local iticket files:

```bash
ls .scratch/.itickets/<tag>/*.md
```

If the folder is empty, skip file matching and proceed with GitHub-only reconciliation.

### Step 4: Reconcile GitHub → local

For each open GitHub issue with the tag, check whether a local file already references it using the [matching rule](skills/itickets/ITICKET-FORMAT.md#matching-rule).

For each open issue with no matching local file:

1. Create a new markdown file in `.scratch/.itickets/<tag>`.
2. Use the [filename convention](skills/itickets/ITICKET-FORMAT.md#filename). Avoid collisions by appending the issue number if needed (e.g. `colors-unappealing-1.md`).
3. Use the [iticket template](skills/itickets/ITICKET-FORMAT.md#template). Set `description:` from the issue body (or title if the body is empty). Set `github-issue:` to the issue URL.

### Step 5: Reconcile local → GitHub

For each `.md` file in `.scratch/.itickets/<tag>`:

1. Read its `github-issue:` line.
2. If it references an open GitHub issue from Step 2, keep the file.
3. Otherwise delete the file. This covers closed issues, deleted issues, issues that lost the tag label, and local files with no `github-issue:` line.

## Constraints

- Do **not** create, close, or edit GitHub issues — only read them.
- Do **not** investigate root cause or expand issue scope when creating local files.
- Do **not** modify unrelated files outside `.scratch/.itickets/<tag>`.
- Report a brief summary when done: tag synced, files added, files removed, files unchanged.
