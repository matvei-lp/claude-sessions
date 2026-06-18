---
name: Do not delete local branches
description: After a PR is merged, do not run `git branch -d` on the local Feature/RAD-XXXX branch — leave it in place.
type: feedback
originSessionId: 2bae577b-581e-41d4-8556-126da6aa09fd
---
After merging a PR, do **not** delete the local `Feature/RAD-XXXX` branch — even if the merge succeeded and the branch is gone from origin. The user keeps local branches around intentionally.

**Why:** User explicitly asked not to delete them (2026-05-12). Even when merged.

**How to apply:** When running a post-merge sync (pull main, etc.), stop after `git pull`. Skip any `git branch -d <feature>` cleanup. If a branch genuinely needs to go (e.g., the user asks), confirm first.
