#!/bin/sh
# Claude sessions git-sync, driven by SessionStart / SessionEnd hooks.
#
#   session_sync.sh start  -> register the jsonl-union merge driver, pull, rebuild Recents
#   session_sync.sh end    -> commit + push, but refuse on a broken state and log failures
#
# Why a script instead of inline hooks: the old one-liners hid push failures
# (`push -q 2>/dev/null`) and blindly `git add -A && commit`-ed conflict markers into
# transcripts. Here failures are logged to tools/sync.log and a conflicted tree is never
# committed. See memory: claude-sessions-git-sync.
set -u
REPO="$HOME/.claude/projects"
LOG="$REPO/tools/sync.log"
cd "$REPO" 2>/dev/null || exit 0

ts() { date +%FT%T; }
log() { echo "$(ts) $*" >> "$LOG"; }

# Real conflict markers only: a JSONL line always starts with '{', so a line beginning
# with 7 '<'/'>' is unambiguously a marker (substring matches in content are ignored).
has_markers() {
    git grep -lE '^(<<<<<<<|>>>>>>>) ' >/dev/null 2>&1
}

ensure_driver() {
    git config merge.jsonl-union.name "union+dedup merge for jsonl transcripts" 2>/dev/null
    git config merge.jsonl-union.driver "python3 '$REPO/tools/jsonl_union_merge.py' %A %B" 2>/dev/null
}

case "${1:-}" in
    start)
        ensure_driver
        git pull --no-edit -q 2>>"$LOG" || log "start: git pull failed"
        if has_markers; then
            log "start: conflict markers present after pull — left for manual review"
        fi
        python3 "$REPO/tools/make_recents.py" >>"$LOG" 2>&1 || log "start: make_recents failed"
        ;;
    end)
        if [ -f .git/MERGE_HEAD ] || [ -n "$(git ls-files -u)" ]; then
            log "end: unfinished merge / unmerged paths — skipping commit & push"
            exit 0
        fi
        if has_markers; then
            log "end: conflict markers in tree — skipping commit & push"
            exit 0
        fi
        git add -A 2>>"$LOG"
        if ! git diff --cached --quiet; then
            git commit -q -m "sync $(hostname -s) $(ts)" 2>>"$LOG" || log "end: commit failed"
        fi
        if ! git push -q 2>>"$LOG"; then
            log "end: git push FAILED (check SSH key / network)"
        fi
        ;;
    *)
        echo "usage: session_sync.sh {start|end}" >&2
        exit 2
        ;;
esac
exit 0
