---
name: pr-flow-radiacode-kmp
description: "PR flow for radiacode-kmp — auto-add vxrossa as reviewer; use gh/GitHub, not the radiacode-ios Bitbucket flow"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 132071b9-2578-4c44-a8a7-5107861c8abd
---

When opening a PR in **radiacode-kmp**, auto-add **vxrossa** (Ivan Basalaev) as reviewer — `gh pr create … --reviewer vxrossa` (or `gh pr edit <n> --add-reviewer vxrossa`).

**Why:** User explicitly asked to auto-add reviewers (2026-06-04); vxrossa approved all his prior PRs here (#4/#5/#6). Also the `pr` skill loads the wrong flow — it pulls the **radiacode-ios** memory (Bitbucket, RAD-, Co-Authored-By, "do not assign reviewers"), which does NOT apply to this repo.

**How to apply:** Use the GitHub flow for radiacode-kmp: `gh` against `Radiacode/radiacode-kmp` (SSH remote); Jira key `RMP-XXXX`; branch `Feature/RMP-XXXX`; base branch **develop** (integration branch — main lags behind); commit/PR title `RMP-XXXX <summary verbatim from Jira>`; **no `Co-Authored-By`** and no AI attribution (per CLAUDE.md); request review from **vxrossa**. Still honor [[require-explicit-approval]] — show the diff + commit-message gate before committing.

**post-merge:** In radiacode-kmp the post-merge routine syncs **develop** (NOT main, and in this repo — not the radiacode-ios path the skill defaults to): `git checkout develop && git pull --ff-only && make`. Don't delete local feature branches; stop & report on non-ff pull.
