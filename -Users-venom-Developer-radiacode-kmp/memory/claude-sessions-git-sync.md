---
name: claude-sessions-git-sync
description: Claude CLI sessions synced venom↔mkozin via a PRIVATE git repo at ~/.claude/projects; auto pull/push hooks
metadata: 
  node_type: memory
  type: project
  originSessionId: 98f573b0-c435-4b42-bcc2-47f75f4802e9
---

Сессии Claude Code шарятся между маками Матвея (venom ↔ mkozin) через **приватный git-репозиторий** (личный GitHub). Настроено 2026-06-18, пришли на смену хрупкой iCloud-схеме.

Устройство:
- `~/.claude/projects` — **это сам git-репозиторий** (не симлинк). Реальные папки сессий — канонические `-Users-venom-Developer-*` (источник правды, коммитятся).
- Второй мак — username **mkozin**. На каждом маке локальные **алиасы-симлинки** `-Users-mkozin-* → -Users-venom-*` (в `.gitignore`, каждый мак создаёт свои). Новые сессии на mkozin пишутся в `-Users-mkozin-*` → симлинк → попадают в каноническую `-Users-venom-*` → коммитятся.
- `titles.json` (в корне репо) — общие заголовки для Recents (`cliSessionId`→title).
- `tools/make_recents.py` — генерит per-machine записи Recents из синканутых `.jsonl` (cwd локализуется под текущий `$HOME`, title из titles.json). Запускать после `git pull`; новые записи видны после **перезапуска приложения** (Recents читается только на старте).

Авто-синк — хуки в `~/.claude/settings.json`:
- **SessionStart** → `git pull` + `make_recents.py`
- **SessionEnd** → `git add -A && commit && push`

Ограничения:
- **Не запускать `claude` на обоих маках одновременно** против одной сессии (иначе git-конфликт на `.jsonl` — но он явный и восстановимый, не тихая потеря).
- Транскрипты содержат код/логи → репо строго **приватный**.
- iCloud-папка `ClaudeProjects` оставлена как бэкап; удалить после стабилизации.

Связано: [[require-explicit-approval]]. Заменяет прежнюю iCloud-схему.
