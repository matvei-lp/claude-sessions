#!/usr/bin/env python3
"""Git merge driver: lossless union of two JSONL transcript versions.

Registered as the `jsonl-union` driver (with args `%A %B`) and bound to `*.jsonl` via
.gitattributes. Git invokes it on a merge conflict; %A is ours AND the output file,
%B is theirs. The merge base is not needed — a union of both sides loses nothing.

Transcripts are append-only logs of one JSON object per line. A textual 3-way merge
produces conflict markers when both sides appended different lines; this driver instead
keeps every unique line, so nothing is ever lost and no markers are committed.

Order: ours preserved verbatim, then theirs-only lines appended. Dedup key is the entry's
`uuid` when present (each transcript entry has a stable uuid), else the full line — so
metadata lines (mode/summary/ai-title, which carry no uuid) dedup by exact content.
Always resolves (exit 0); on any unexpected error it falls back to ours unchanged.
"""
import json
import sys


def read_lines(path):
    try:
        with open(path, errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        return []


def key(line):
    try:
        obj = json.loads(line)
        u = obj.get("uuid")
        if u:
            return ("uuid", u)
    except Exception:
        pass
    return ("raw", line)


def main(argv):
    # argv is sys.argv[1:] -> [ours(%A, also the output file), theirs(%B)]
    if len(argv) < 2:
        return 0
    ours_path, theirs_path = argv[0], argv[1]
    ours = read_lines(ours_path)
    theirs = read_lines(theirs_path)

    seen = set()
    merged = []
    for line in ours + theirs:
        k = key(line)
        if k in seen:
            continue
        seen.add(k)
        merged.append(line)

    with open(ours_path, "w") as f:
        f.write("\n".join(merged))
        if merged:
            f.write("\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception:
        # Never block a pull on a driver bug — leave ours as-is, report resolved.
        sys.exit(0)
