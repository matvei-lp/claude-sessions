# claude-sessions

Synced Claude Code CLI session store, shared across machines (venom ↔ mkozin).

## Layout
- `-Users-venom-Developer-*/` — canonical per-project session folders (the real `.jsonl` transcripts). Named after the **venom** mac's paths; this is the committed source of truth.
- `-Users-mkozin-*` — per-machine alias symlinks → the canonical `-Users-venom-*` folders, so `claude --resume` finds sessions under the local username. **Gitignored** (each machine recreates its own).
- `titles.json` — curated sidebar titles (`cliSessionId` → title), shared.
- `tools/make_recents.py` — regenerates the desktop "Recents" wrapper records from these transcripts, with machine-local `cwd` and shared titles.

## Sync
Auto via Claude Code hooks (`~/.claude/settings.json`):
- **SessionStart** → `git pull` + `make_recents.py`
- **SessionEnd** → `git add -A && commit && push`

New sessions created on either mac land in the canonical folder (via the local alias symlink) and sync. Cross-mac sessions appear in the sidebar after the next app launch (the app reads Recents only at startup).

## New machine setup
1. `git clone <remote> ~/.claude/projects` (back up any existing dir first).
2. Create local alias symlinks for this machine's username (see `tools/`).
3. `python3 ~/.claude/projects/tools/make_recents.py` and restart the app.

⚠️ Do not run `claude` on two machines simultaneously against the same session.
