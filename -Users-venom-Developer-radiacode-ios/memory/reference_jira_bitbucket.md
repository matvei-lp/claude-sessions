---
name: Jira and Bitbucket coordinates
description: Where to look up tickets (Jira) and open PRs (Bitbucket) for the radiacode-ios project, plus the user's identifiers.
type: reference
originSessionId: 2bae577b-581e-41d4-8556-126da6aa09fd
---
**Jira instance:** https://radiacode.atlassian.net
- User's Atlassian email: matvei@radiacode.com
- Ticket key prefix: `RAD-` (e.g., `RAD-1167`)
- Auth via REST API: basic auth with `JIRA_EMAIL` + `JIRA_TOKEN` env vars. Token created at https://id.atlassian.com/manage-profile/security/api-tokens
- Read a ticket: `curl -u "$JIRA_EMAIL:$JIRA_TOKEN" "$JIRA_URL/rest/api/3/issue/RAD-XXXX"`

**Bitbucket repo:** bitbucket.org/radiacode/radiacode-ios
- Bitbucket username: `mvkozin`
- Email: `matvei@radiacode.com`
- App passwords are deprecated (since Sep 2025). Use **API tokens with scopes** created at https://id.atlassian.com/manage-profile/security/api-tokens → "Create API token with scopes" → product Bitbucket. Required scopes: `read:repository:bitbucket`, `write:repository:bitbucket`, `read:pullrequest:bitbucket`, `write:pullrequest:bitbucket`.
- Env vars: `BITBUCKET_EMAIL`, `BITBUCKET_API_TOKEN`.
- **Auth identifier differs by transport** (this caught me once — verify next time):
  - REST API: basic auth with **email** + token. `curl -u "$BITBUCKET_EMAIL:$BITBUCKET_API_TOKEN" https://api.bitbucket.org/...`
  - Git over HTTPS: **username** (`mvkozin`) + token. Push example: `git -c credential.helper='!f() { echo "username=mvkozin"; echo "password=$BITBUCKET_API_TOKEN"; }; f' push -u origin <branch>`
- Create PR: `POST https://api.bitbucket.org/2.0/repositories/radiacode/radiacode-ios/pullrequests` with body `{"title": ..., "source": {"branch": {"name": "..."}}, "destination": {"branch": {"name": "main"}}, "close_source_branch": true}`
- List PRs: `GET https://api.bitbucket.org/2.0/repositories/radiacode/radiacode-ios/pullrequests`

**Workflow when user gives a ticket number (e.g., "RAD-1234"):**
1. Read ticket via Jira API, summarize what needs doing in one paragraph.
2. Wait for user's "go" or scope corrections.
3. Branch from `main` as `Feature/RAD-XXXX` (confirm naming — see project conventions below).
4. Implement, build to verify.
5. Show diff, wait for confirmation.
6. Only then push + open PR via Bitbucket API.

**Conventions:**
- Branch name: `Feature/RAD-XXXX` (no slug — just the ticket key).
- Commit message: `RAD-XXXX <summary>`, where `<summary>` is taken verbatim from the Jira ticket's `fields.summary`. Do NOT paraphrase or translate.
- PR base: `main`.
- PR title: same as commit message — `RAD-XXXX <summary>`.
- Default reviewer: none. Create PRs without a `reviewers` field — the user assigns reviewers manually after the PR is open.
