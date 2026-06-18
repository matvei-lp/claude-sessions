---
name: No Co-Authored-By in commits
description: When creating commits for this project, do not add `Co-Authored-By: Claude ...` trailer. Use plain commit message only.
type: feedback
originSessionId: bec000d5-516c-413b-b57a-4b48aef09bfc
---
When creating commits for this project (including via `/pr` flow), do NOT add the `Co-Authored-By: Claude ...` trailer. Use plain commit message only.

**Why:** User explicitly requested this on 2026-05-18 during RAD-1177 PR: "Не пиши о себе в коммите". They prefer commit history without LLM-coauthor noise.

**How to apply:** When the `/pr` skill or general commit flow includes a Co-Authored-By trailer in its template, omit that trailer. Just use the bare commit message (e.g., `RAD-XXXX <summary>`).
