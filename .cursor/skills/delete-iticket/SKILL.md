---
name: delete-iticket
description: Closes a GitHub issue for a given tag and deletes its local `.scratch/.itickets/<tag>` file when present. Use when the user wants to delete, close, remove, or discard an iticket, quickssue, idea, or feature.
disable-model-invocation: true
---

# Delete Iticket

Close a tagged issue on GitHub and remove its local file from `.scratch/.itickets/<tag>`.

Shared file format and matching rules: [ITICKET-FORMAT.md](skills/itickets/ITICKET-FORMAT.md).

## Parse user input

Extract **tag** and **target** from the user's message:

1. Strip optional leading filler: `delete`, `close`, `remove`, `destroy`, `discard`.
2. **Tag** — first remaining word (lowercase).
3. **Target** — everything after the tag (issue number, URL, local filename, or title/description fragment).

Examples:

| Input | Tag | Target |
|-------|-----|--------|
| `quickssue 42` | `quickssue` | issue `42` |
| `feature dark-mode-toggle` | `feature` | filename `dark-mode-toggle.md` |
| `idea cache search broken` | `idea` | description match |

If no tag can be parsed, ask the user. If tag is present but target is ambiguous, resolve using Step 1 below.

## Workflow

```
Task progress:
- [ ] Step 1: Resolve the target iticket
- [ ] Step 2: Close the GitHub issue
- [ ] Step 3: Delete the local file
```

### Step 1: Resolve the target iticket

Determine the GitHub issue number from the target:

- **Issue number or URL** — use directly (e.g. `42`, `https://github.com/owner/repo/issues/42`).
- **Local filename** — read `.scratch/.itickets/<tag>/<filename>.md` and take the value from its `github-issue:` line.
- **Title or description** — list open issues for the tag and local files, then pick the best match:

```bash
gh issue list --label <tag> --state open --json number,title,url
```

If multiple matches exist, ask the user to pick one. If none match, stop and report that no iticket was found for that tag.

### Step 2: Close the GitHub issue

Close the issue with `gh`:

```bash
gh issue close <number>
```

- Use the issue number only (not the full URL).
- If the issue is already closed, skip closing and proceed to Step 3.
- Do **not** close issues that are unrelated to the user's request.

### Step 3: Delete the local file

In `.scratch/.itickets/<tag>`, delete any `.md` file whose `github-issue:` line matches the issue number or URL per the [matching rule](skills/itickets/ITICKET-FORMAT.md#matching-rule).

If no matching local file exists, that is fine — report that the GitHub issue was closed and no local file was found.

## Constraints

- Do **not** investigate root cause, explore the codebase, or expand scope.
- Do **not** close or delete unrelated issues or files.
- Do **not** modify files outside `.scratch/.itickets/<tag>`.
- Report a brief summary when done: tag, issue closed (or already closed), local file deleted (or none found).
