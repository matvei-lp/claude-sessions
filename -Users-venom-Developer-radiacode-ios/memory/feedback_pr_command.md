---
name: /pr-XXXX command
description: When user says "/pr-XXXX" (or "сделай PR RAD-XXXX"), wrap the current uncommitted changes into a Feature/RAD-XXXX branch and open a Bitbucket PR.
type: feedback
originSessionId: 2bae577b-581e-41d4-8556-126da6aa09fd
---
When the user invokes `/pr-XXXX` (where XXXX is a Jira ticket number, e.g. `/pr-1169`) — or any clear equivalent like "сделай PR для RAD-1169":

**Precondition:** there must be uncommitted changes in `/Users/mkozin/Developer/radiacode-ios`. The uncommitted diff IS the implementation. If the working tree is clean, stop and ask — do not proceed to implement on your own.

**Env vars:** `JIRA_URL`, `JIRA_EMAIL`, `JIRA_TOKEN`, `BITBUCKET_EMAIL`, `BITBUCKET_API_TOKEN` are loaded via `.claude/settings.local.json` `env` block (gitignored). Do NOT `source ~/.zshrc` — that triggers harness "evaluates arguments as shell code" prompts.

**Sequence:**

1. **Read the Jira ticket** via REST API to get the exact `fields.summary`:
   ```
   curl -sS -u "$JIRA_EMAIL:$JIRA_TOKEN" "$JIRA_URL/rest/api/3/issue/RAD-XXXX?fields=summary,status"
   ```
2. **Show the user**: ticket summary + diff stat (`git diff --stat`). Ask for confirmation: "коммитим как `RAD-XXXX <summary>`?" Do NOT skip this gate.
3. After user's "да":
   - `git checkout -b Feature/RAD-XXXX` (uncommitted changes follow into the new branch).
   - Build to verify: `xcodebuild -project RadiaCode.xcodeproj -scheme Radiacode -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.5' -configuration Debug build CODE_SIGNING_ALLOWED=NO`. If `RadiaCode.xcodeproj` is missing, run `xcodegen generate` first.
   - `git add` only the listed modified files (not `-A`).
   - Commit with message `RAD-XXXX <summary verbatim from Jira>` plus the standard `Co-Authored-By` trailer.
   - Push via Bitbucket username (NOT email — see reference_jira_bitbucket.md):
     ```
     git -c credential.helper='!f() { echo "username=mvkozin"; echo "password=$BITBUCKET_API_TOKEN"; }; f' push -u origin Feature/RAD-XXXX
     ```
   - Create PR via Bitbucket REST API (email + token here, not username):
     ```
     curl -u "$BITBUCKET_EMAIL:$BITBUCKET_API_TOKEN" -X POST -H "Content-Type: application/json" \
       "https://api.bitbucket.org/2.0/repositories/radiacode/radiacode-ios/pullrequests" \
       -d '{"title": "RAD-XXXX <summary>", "source": {"branch": {"name": "Feature/RAD-XXXX"}}, "destination": {"branch": {"name": "main"}}, "close_source_branch": true}'
     ```
4. **Report PR URL** to the user. Do not assign reviewers — user does that manually.

**Why:** User wants a one-shot wrapper for the very common "I've made changes, now make a PR for ticket X" flow. Confirmed 2026-05-12.

**Gates** (do not remove without asking):
- ONE confirmation gate total: "Открываем PR для RAD-XXXX?" → user says "Да". After that: branch + build + commit + push + create PR — all in sequence, no further questions. Never ask separately about push or PR creation.
