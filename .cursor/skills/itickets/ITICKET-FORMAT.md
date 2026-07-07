# Iticket Format

An **iticket** is an instance of a git issue that has an **itag**: quickssues, ideas, features, or any other type distinguished by its itag. Each iticket is a markdown file under `.scratch/.itickets/<itag>/`, linked to a GitHub issue with the matching label.

Create `.scratch/.itickets/<itag>` lazily — only when the first iticket for that itag is written.

## Itag

The **itag** is the first substantive word in the user's input after optional filler (`new`, `a`, `an`, `create`, `add`). It becomes:

- the GitHub issue **label** (exact match, lowercase)
- the local subfolder name under `.scratch/.itickets/`

Examples: `quickssue`, `idea`, `feature`

## Template

```markdown
description:

github-issue:
```

- **description:** One or two sentences — lightly edited from what the user said. Minor grammar and spelling fixes only; do not expand scope or add acceptance criteria unless the user provided them.
- **github-issue:** GitHub issue number (e.g. `1`) or full URL (e.g. `https://github.com/owner/repo/issues/1`). Set when the GitHub issue exists; required for sync and delete matching.

When creating a new iticket locally before the GitHub issue exists, write `description:` first and add `github-issue:` after the issue is created.

## Filename

Three lowercase words from the issue summary, joined by hyphens, ending in `.md`.

Examples: `login-button-broken.md`, `colors-unappealing-dull.md`

When syncing from GitHub and a filename collision occurs, append the issue number (e.g. `colors-unappealing-1.md`).

## Matching rule

A local file represents a GitHub issue when its `github-issue:` value equals the issue number or the issue URL.

## GitHub label

Each itag maps 1:1 to a GitHub label. If the label does not exist when creating an iticket, create it:

```bash
gh label create <itag> --description "Iticket: <itag>" --color "ededed"
```

Known itags may use custom label metadata. Example for quickssues:

```bash
gh label create quickssue --description "Casual quick-capture issue" --color "FBCA04"
```
