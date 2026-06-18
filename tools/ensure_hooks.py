#!/usr/bin/env python3
"""Self-migration for the sessions-sync hooks. Called from make_recents.py.

~/.claude/settings.json is per-machine and NOT synced via git, so a machine still running
the old inline SessionStart/SessionEnd one-liners can't be updated remotely. This module —
which DOES sync (it lives in the repo, and the old hook runs make_recents.py) — repoints
those two hooks at tools/session_sync.sh and registers the jsonl-union merge driver in the
local .git/config. Both steps are idempotent: a no-op once a machine is already migrated.
"""
import json
import os
import subprocess

HOME = os.path.expanduser("~")
REPO = os.path.join(HOME, ".claude/projects")
SETTINGS = os.path.join(HOME, ".claude/settings.json")
START_CMD = 'sh "$HOME/.claude/projects/tools/session_sync.sh" start'
END_CMD = 'sh "$HOME/.claude/projects/tools/session_sync.sh" end'


def register_driver():
    """Register the jsonl-union merge driver locally (config is not synced)."""
    driver = "python3 '" + os.path.join(REPO, "tools/jsonl_union_merge.py") + "' %A %B"
    for key, val in (("merge.jsonl-union.name", "union+dedup merge for jsonl transcripts"),
                     ("merge.jsonl-union.driver", driver)):
        try:
            subprocess.run(["git", "-C", REPO, "config", key, val], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass


def _is_old(event, cmd):
    """True if `cmd` is an old inline sync hook for `event` (and not already migrated)."""
    if "session_sync.sh" in cmd or ".claude/projects" not in cmd:
        return False
    if event == "SessionStart":
        return "make_recents.py" in cmd or ("git" in cmd and "pull" in cmd)
    if event == "SessionEnd":
        return "push" in cmd or "add -A" in cmd
    return False


def migrate_settings():
    """Repoint old SessionStart/SessionEnd hook commands at session_sync.sh (idempotent)."""
    try:
        with open(SETTINGS) as f:
            raw = f.read()
        data = json.loads(raw)
    except Exception:
        return
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        return
    new_for = {"SessionStart": START_CMD, "SessionEnd": END_CMD}
    changed = False
    for event, newcmd in new_for.items():
        for group in hooks.get(event, []) or []:
            for h in group.get("hooks", []) or []:
                if h.get("type") == "command" and _is_old(event, h.get("command", "")):
                    h["command"] = newcmd
                    changed = True
    if not changed:
        return
    try:
        with open(SETTINGS + ".bak", "w") as f:   # keep the pre-migration version
            f.write(raw)
        with open(SETTINGS, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    except Exception:
        pass


def run():
    register_driver()
    migrate_settings()


if __name__ == "__main__":
    run()
