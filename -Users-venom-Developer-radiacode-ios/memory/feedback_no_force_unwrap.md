---
name: No force unwrap in proposed code
description: Never propose Swift code containing `!` (force unwrap, IUO access, try!). Use safe alternatives.
type: feedback
originSessionId: b07fbd7a-32ba-49fd-8d44-e7cc32f89be2
---
Never propose Swift code that uses `!`:
- force unwrap (`array[i]!`, `optional!`)
- implicitly-unwrapped optionals access
- `try!`
- `as!` (force cast)

**Why:** force unwraps crash in production; the user does not want fragile code shown as a suggestion, even if "obviously safe" in context.

**How to apply:** when writing or refactoring Swift, prefer `guard let`, `if let`, `??`, `try?`, `as?`, or restructure to avoid the optional entirely. Examples to avoid: `groups[groups.indices.last!]`, `events.first!`, `try! decoder.decode(...)`. Replace with `groups.indices.last.map { groups[$0] }`, `events.first.map { ... }`, `try?` + handling, etc. Applies in all proposals and final edits — no exceptions for "this can't be nil here".
