# Memory

- [No worktrees](feedback_no_worktrees.md) — work in the main repo path, not isolated worktrees.
- [Jira and Bitbucket coordinates](reference_jira_bitbucket.md) — Jira URL, repo, auth env vars, ticket workflow for RAD-XXXX requests.
- [Do not delete local branches](feedback_no_local_branch_delete.md) — leave merged Feature/RAD-XXXX branches in place after pull.
- [/post-merge routine](feedback_post_merge_routine.md) — `git checkout main && git pull --ff-only && make` after a PR is merged.
- [/pr-XXXX command](feedback_pr_command.md) — wrap current uncommitted changes into a Feature/RAD-XXXX branch and open a Bitbucket PR.
- [Propose before applying](feedback_propose_before_apply.md) — показывать код/diff в чате; применять ТОЛЬКО когда сообщение пользователя — ровно одно слово «применить» (ни «сделай», ни «давай», ни кнопка не триггерят).
- [No force unwrap](feedback_no_force_unwrap.md) — never propose Swift code with `!` (force unwrap, `try!`, `as!`); use safe alternatives.
- [Device protocol reference](reference_device_protocol.md) — RadiaCode USB/Bluetooth protocol at `docs/Protocol.pdf` (287 pp), also documented in CLAUDE.md.
- [No Co-Authored-By](feedback_no_coauthor.md) — omit `Co-Authored-By: Claude ...` trailer in commits.
- [No guesswork](feedback_no_guesswork.md) — никогда не реализовывать по догадкам; читать Protocol.pdf из вложений Jira-тикета.
- [Respond in Russian](feedback_respond_in_russian.md) — всегда отвечать на русском, независимо от языка вопроса.
- [@ViewBuilder stored property](feedback_viewbuilder_stored_property.md) — использовать `@ViewBuilder let content: Content`, не `() -> Content`; явный init не нужен.
- [No abbreviated variable names](feedback_no_abbreviated_names.md) — не использовать сокращённые имена переменных типа `f`, `v`, `u`, `d` и т.п.; всегда давать полные описательные имена (например `formatted`, `value`, `unit`, `dose`).
- [KMP migration](project_kmp_migration.md) — переезд на Kotlin Multiplatform; структура Jira-проекта RMP (инициативы Core/Android/iOS/Web) и граница Core vs платформы.
