#!/usr/bin/env python3
"""Materialize Claude Code desktop "Recents" records from synced session transcripts.

The desktop app builds its sidebar at launch from per-machine wrapper records at
  ~/Library/Application Support/Claude/claude-code-sessions/<ws>/<ws>/local_<uuid>.json
Each record links to a CLI session .jsonl via `cliSessionId` and carries a machine-local
`cwd` + a `title`. Transcripts + titles.json sync via git; this script regenerates the
local records for any session that doesn't have one yet (skips existing -> no duplicates)
and backfills createdAt/lastActivityAt on existing records from the transcript timestamps,
so Recents stays correctly sorted after a pull on another machine.

Run after `git pull`. New records show in the sidebar after the next app launch.
"""
import json
import os
import re
import glob
import uuid
from datetime import datetime

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


def session_times(path, fallback_ms):
    """(createdAt, lastActivityAt) in ms from transcript `timestamp`s, else fallback.

    Content timestamps are identical on every machine; file mtime is not (it tracks
    the git checkout), so deriving from the transcript keeps Recents sorted correctly
    after a pull on another Mac.
    """
    first = last = None
    try:
        with open(path, errors="replace") as f:
            for line in f:
                try:
                    ts = json.loads(line).get("timestamp")
                except Exception:
                    continue
                if not ts:
                    continue
                try:
                    ms = int(datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp() * 1000)
                except Exception:
                    continue
                if first is None:
                    first = ms
                last = ms
    except Exception:
        pass
    return (first or fallback_ms, last or first or fallback_ms)


def localize(cwd):
    """Rewrite /Users/<anyone>/rest -> $HOME/rest when that path exists on this machine."""
    m = re.match(r"^/Users/[^/]+/(.*)$", cwd or "")
    if m:
        cand = os.path.join(HOME, m.group(1))
        if os.path.isdir(cand):
            return cand
    return cwd


def main():
    try:                                  # self-migrate old hooks + register merge driver
        import ensure_hooks
        ensure_hooks.run()
    except Exception:
        pass
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

    # Map cli session id -> transcript path (skip per-machine alias symlinks).
    cli_to_jsonl = {}
    for proj in glob.glob(os.path.join(STORE, "-Users-*")):
        if os.path.islink(proj):                 # skip per-machine alias symlinks
            continue
        for jl in glob.glob(os.path.join(proj, "*.jsonl")):
            cli_to_jsonl[os.path.basename(jl)[:-6]] = jl

    # Backfill timestamps on existing records from their transcript, and note which
    # clis already have a record so we don't create duplicates below.
    have = set()
    fixed = 0
    for p in glob.glob(os.path.join(SESS, "*", "*", "local_*.json")):
        try:
            rec = json.load(open(p))
        except Exception:
            continue
        cli = rec.get("cliSessionId")
        if cli:
            have.add(cli)
        jl = cli_to_jsonl.get(cli)
        if not jl:
            continue
        fallback = rec.get("createdAt") or int(os.path.getmtime(jl) * 1000)
        created_ms, last_ms = session_times(jl, fallback)
        if rec.get("createdAt") != created_ms or rec.get("lastActivityAt") != last_ms:
            rec.update({"createdAt": created_ms, "lastActivityAt": last_ms, "lastFocusedAt": last_ms})
            json.dump(rec, open(p, "w"))
            fixed += 1

    created = 0
    for cli, jl in cli_to_jsonl.items():
        if cli in have:
            continue
        cwd = localize(jget(jl, "cwd"))
        if not cwd:
            continue
        created_ms, last_ms = session_times(jl, int(os.path.getmtime(jl) * 1000))
        nl = "local_" + str(uuid.uuid4())
        rec = json.loads(json.dumps(tmpl))
        rec.update({
            "sessionId": nl, "cliSessionId": cli, "cwd": cwd, "originCwd": cwd,
            "title": titles.get(cli) or ("Session " + cli[:8]),
            "titleSource": "auto", "isArchived": False,
            "createdAt": created_ms, "lastActivityAt": last_ms, "lastFocusedAt": last_ms,
        })
        json.dump(rec, open(os.path.join(parent, nl + ".json"), "w"))
        have.add(cli)
        created += 1

    print(f"make-recents: created {created} record(s), fixed {fixed} timestamp(s)")


if __name__ == "__main__":
    main()
