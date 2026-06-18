---
name: /post-merge routine
description: When user says "/post-merge" (or just "post-merge"), run the post-merge sync sequence after a PR has been merged on Bitbucket.
type: feedback
originSessionId: 2bae577b-581e-41d4-8556-126da6aa09fd
---
When the user says `/post-merge` (or any close variant — "post-merge", "запусти post-merge", etc.), run this exact sequence in `/Users/mkozin/Developer/radiacode-ios`:

```
git checkout main
git pull --ff-only
make
```

That's it. Do not also `git branch -d` the merged feature branch (see the no-local-branch-delete memory).

**Why:** User wants a one-word command for the repeatable sync after merging a PR. Established 2026-05-12 right after RAD-1169 was merged. `make` regenerates the Xcode project (`xcodegen generate`) and opens it in Xcode — needed so the IDE picks up post-merge state.

**How to apply:**
- Run the three commands as-is.
- If `git pull --ff-only` fails (non-fast-forward), stop and report — don't force or merge.
- If `make` errors, surface the tail of the output. Don't silently retry.
- Do not delete any local branches as part of this flow.
