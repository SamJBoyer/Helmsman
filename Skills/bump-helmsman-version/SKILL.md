---
name: bump-helmsman-version
description: Bumps the Helmsman canon version from git tags after fixing spelling, minor grammar, and broken XML tags; updates canon/tag.md, commits current work, creates an annotated tag whose -m message is the rest of the prompt after bump-helmsman, and pushes the tag. Use only when the user invokes bump helmsman version, bumps the Helmsman version, or tags a new Helmsman release.
disable-model-invocation: true
---

# Bump Helmsman Version

Bump the Helmsman version by looking at the tags in the git history and incrementing the tag by 1. For example, v0.0.5 becomes v0.0.6, and v0.0.9 becomes v0.1.0. Make a commit of the current work, then tag the commit, and then push the tag. Be sure to replace the file canon/tag.md with the new tag.

## Preconditions — stop if unmet

This skill can only be called if both are true:

1. `canon/c_hDocs` is present in the repo (directory exists).
2. The project's name is `"Helmsman"`.

Resolve the project name from the git remote repo name (basename of `origin` URL without `.git`), e.g. `https://github.com/SamJBoyer/Helmsman.git` → `Helmsman`.

If either condition fails, **stop**. Do not bump, commit, tag, or push. Report which condition failed.

## Scope — do only this

When this skill is invoked and preconditions pass: proofread and fix the release content, compute the next tag, write `canon/tag.md`, commit current work, tag that commit with the prompt description as `-m`, push the tag. Do **not** rewrite meaning, add features, or change hDocs unless those files are already part of the current uncommitted work being committed.

## Parse tag message from the prompt

The rest of the prompt following `bump-helmsman` (or `bump helmsman version` / equivalent invocation) may contain a description of the changes. Make this the tag `-m` message.

1. Take the user message text after the skill invocation / skill name.
2. Trim leading/trailing whitespace.
3. Use that string verbatim as `MESSAGE` for `git tag -a … -m`.
4. If nothing follows the invocation (empty description), stop and ask the user for a short description of the changes before tagging. Do not invent a message.

## Pre-bump cleanup

Before bumping the version, correct any spelling mistakes or minor grammar work. Also fix any broken XML tags.

Scope of cleanup:

- Everything under `canon/` (especially `canon/c_hDocs/` and `canon/instructions/`)
- Any other files already in the current uncommitted work that will be included in the bump commit

Allowed fixes only:

- Spelling mistakes
- Minor grammar (punctuation, agreement, small clarity tweaks that do not change meaning)
- Broken XML / XML-like tags (mismatched, unclosed, or mistyped tags such as `<glossary>` / `</glossary>`)

Do **not** rephrase for style, restructure documents, or invent new content. If a wording change would alter meaning, leave it and report it instead of “fixing” it.

## Version increment

1. Fetch tags: `git fetch --tags`
2. List version tags matching `vMAJOR.MINOR.PATCH` (digits only).
3. Take the highest tag by version order (not by date).
4. Increment by 1 on the patch digit:
   - `vX.Y.Z` → `vX.Y.(Z+1)` when `Z < 9`
   - `vX.Y.9` → `vX.(Y+1).0` when `Y < 9`
   - `vX.9.9` → `v(X+1).0.0`

If no matching tags exist, stop and report that there is no prior version tag to increment.

## Workflow

```
Task progress:
- [ ] Step 1: Verify preconditions
- [ ] Step 2: Parse MESSAGE from the rest of the prompt
- [ ] Step 3: Correct spelling, minor grammar, and broken XML tags
- [ ] Step 4: Resolve next version from git tags
- [ ] Step 5: Replace canon/tag.md with the new tag
- [ ] Step 6: Commit current work
- [ ] Step 7: Tag the commit with -m MESSAGE
- [ ] Step 8: Push the tag
- [ ] Step 9: Report old tag → new tag, commit SHA, MESSAGE, and cleanup fixes
```

### Step 1: Verify preconditions

Confirm `canon/c_hDocs` exists and the project name is `Helmsman`. Stop if not.

### Step 2: Parse MESSAGE from the rest of the prompt

Extract the description of the changes from the rest of the prompt following `bump-helmsman`. That string is `MESSAGE`. If empty, stop and ask for a description.

### Step 3: Correct spelling, minor grammar, and broken XML tags

Add to correct any spelling mistakes or minor grammar work before you bump the version. Also fix any broken XML tags.

Scan the cleanup scope above, apply allowed fixes, and keep a short list of what changed for the final report.

### Step 4: Resolve next version

Fetch tags and compute the next tag with the increment rules above. Call the previous highest tag `OLD` and the result `NEW`.

### Step 5: Replace canon/tag.md

Overwrite `canon/tag.md` so its entire contents are exactly the new tag string (e.g. `v0.0.3`) and a trailing newline. No other text.

### Step 6: Commit current work

Stage **all** current work in the working tree (including cleanup edits, `canon/tag.md`, and any other pending changes), then create a commit.

Commit message style: short, imperative; mention the version bump, e.g. `Bump Helmsman version to v0.0.3`.

Only create the commit when this skill was invoked. Do not push the branch unless needed for the tag push to succeed.

### Step 7: Tag the commit with -m MESSAGE

Create an annotated tag named `NEW` on `HEAD`, using the prompt description as the tag message:

```bash
git tag -a NEW -m "MESSAGE"
```

Do not move or overwrite an existing tag. If `NEW` already exists, stop and report the conflict. Do not paraphrase `MESSAGE`.

### Step 8: Push the tag

```bash
git push origin NEW
```

Push the tag only (this publishes the tagged commit). Do not force-push.

### Step 9: Report

Report `OLD` → `NEW`, the commit SHA, `MESSAGE`, that the tag was pushed, and a brief list of spelling/grammar/XML fixes (or that none were needed).

## Constraints

- Never run this skill when `canon/c_hDocs` is missing or the project name is not `Helmsman`.
- Never invent a tag `-m` message; require it from the rest of the prompt (or ask if missing).
- Never skip the pre-bump spelling/grammar/XML cleanup pass.
- Never skip updating `canon/tag.md` before the commit.
- Never force-push tags or rewrite existing tags.
- Under `canon/`, only apply spelling, minor grammar, and broken-XML fixes (plus writing `canon/tag.md`). Do not make other canon edits.
- Follow the user's normal git safety rules (no `git config` changes, no `--no-verify` unless they ask).
