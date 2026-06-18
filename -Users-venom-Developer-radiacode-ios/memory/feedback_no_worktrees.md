---
name: No worktrees
description: User opens the main repo in Xcode; changes made in an isolated worktree are invisible to them, so never work in a worktree for this project.
type: feedback
originSessionId: 2bae577b-581e-41d4-8556-126da6aa09fd
---
Always operate inside `/Users/mkozin/Developer/radiacode-ios` (the main repo working tree). Do not work inside `.claude/worktrees/*`.

**Why:** The user keeps Xcode open against the main repo path. When a session runs in an isolated worktree, changes don't appear in their Xcode session and they can't review the work. They explicitly asked to stop using worktrees (2026-05-12).

**How to apply:**
- If a session starts in a worktree (the system prompt says "You are operating in a git worktree"), warn the user up front and offer to either (a) port the work to the main repo with `git apply` patches, or (b) ask them to relaunch the session without worktree isolation.
- Don't proactively create new worktrees.
- When the user starts a fresh session and the harness has spawned a worktree anyway, do work in the main repo path and use the worktree only as the cwd. Mirror finished diffs to the main repo before declaring done.
