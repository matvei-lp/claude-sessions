#!/usr/bin/env python3
"""Materialize Claude Code desktop "Recents" records from synced session transcripts.

The desktop app builds its sidebar at launch from per-machine wrapper records at
  ~/Library/Application Support/Claude/claude-code-sessions/<ws>/<ws>/local_<uuid>.json
Each record links to a CLI session .jsonl via `cliSessionId` and carries a machine-local
`cwd` + a `title`. Transcripts + titles.json sync via git; this script regenerates the
local records for any session that doesn't have one yet (skips existing -> no duplicates).

Run after `git pull`. New records show in the sidebar after the next app launch.
"""
import json
import os
import re
import glob
import uuid

HOME = os.path.expanduser("~")
SESS = os.path.join(HOME, "Library/Application Support/Claude/claude-code-sessions")
STORE = os.path.join(HOME, ".claude/projects")          # this file lives in STORE/tools
TITLES_PATH = os.path.join(STORE, "titles.json")


def load_titles():
    try:
        return {t["cli"]: t["title"] for t in json.load(open(TITLES_PATH))}
    except Exception:
        return {}


def find_template():
    """Largest existing record is the richest template (carries remoteMcpServersConfig)."""
    for p in sorted(glob.glob(os.path.join(SESS, "*", "*", "local_*.json")),
                    key=os.path.getsize, reverse=True):
        try:
            return json.load(open(p)), os.path.dirname(p)
        except Exception:
            continue
    return None, None


def existing_clis():
    out = set()
    for p in glob.glob(os.path.join(SESS, "*", "*", "local_*.json")):
        try:
            out.add(json.load(open(p)).get("cliSessionId"))
        except Exception:
            pass
    return out


def jget(path, field):
    try:
        with open(path, errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get(field):
                    return d[field]
    except Exception:
        pass
    return None


def localize(cwd):
    """Rewrite /Users/<anyone>/rest -> $HOME/rest when that path exists on this machine."""
    m = re.match(r"^/Users/[^/]+/(.*)$", cwd or "")
    if m:
        cand = os.path.join(HOME, m.group(1))
        if os.path.isdir(cand):
            return cand
    return cwd


def main():
    titles = load_titles()
    tmpl, parent = find_template()
    if tmpl is None:
        tmpl = {
            "remoteMcpServersConfig": [], "sessionSettings": {}, "model": "claude-opus-4-8",
            "effort": "high", "permissionMode": "default", "completedTurns": 0,
            "alwaysAllowedReasons": [], "sessionPermissionUpdates": [],
        }
        parent = os.path.join(SESS, str(uuid.uuid4()), str(uuid.uuid4()))
        os.makedirs(parent, exist_ok=True)

    have = existing_clis()
    created = 0
    for proj in glob.glob(os.path.join(STORE, "-Users-*")):
        if os.path.islink(proj):                 # skip per-machine alias symlinks
            continue
        for jl in glob.glob(os.path.join(proj, "*.jsonl")):
            cli = os.path.basename(jl)[:-6]
            if cli in have:
                continue
            cwd = localize(jget(jl, "cwd"))
            if not cwd:
                continue
            mt = int(os.path.getmtime(jl) * 1000)
            nl = "local_" + str(uuid.uuid4())
            rec = json.loads(json.dumps(tmpl))
            rec.update({
                "sessionId": nl, "cliSessionId": cli, "cwd": cwd, "originCwd": cwd,
                "title": titles.get(cli) or ("Session " + cli[:8]),
                "titleSource": "auto", "isArchived": False,
                "createdAt": mt, "lastActivityAt": mt, "lastFocusedAt": mt,
            })
            json.dump(rec, open(os.path.join(parent, nl + ".json"), "w"))
            have.add(cli)
            created += 1

    print(f"make-recents: created {created} record(s)")


if __name__ == "__main__":
    main()
