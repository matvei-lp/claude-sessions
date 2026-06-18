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
- **SessionStart** → `git pull --no-edit || merge --abort` (abort, чтобы конфликт не оставил полу-слитое дерево, иначе следующий `add -A` закоммитит маркеры) + `make_recents.py`
- **SessionEnd** → `git add -A && commit && push`; сбой push логируется в `~/.claude/sync-push.log` (вне репо). Если push молча «не работает» — смотреть этот лог первым делом.

Remote: `git@github.com:matvei-lp/claude-sessions.git` (SSH). Ключ `~/.ssh/id_ed25519` (отпечаток `SHA256:viD0…WjcI`, на GitHub зовётся «Mac M5»). **Ключ под passphrase** → push из хука неинтерактивный и молча падал (`Permission denied (publickey)`), т.к. ключ не был в agent. Лечится: `~/.ssh/config` с `UseKeychain yes` + `AddKeysToAgent yes` и разовый `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` (пароль уходит в Keychain, дальше push работает и после ребута). Проверка: `ssh -T git@github.com` → `Hi matvei-lp!`.

Разрешение конфликта транскрипта (одна сессия правилась на двух маках): `.jsonl` — append-only лог; сравнить версии (`comm` по отсортированным строкам). Обычно одна — надмножество другой (на маке, где сессию дописывали, больше строк; на втором лишь сгенерился `ai-title`/`mode`). Тогда `git checkout --ours/--theirs` нужной версии = **lossless**. Сверять числом уникальных строк, а не префиксом (порядок служебных записей различается).

Ограничения:
- **Не запускать `claude` на обоих маках одновременно** против одной сессии (иначе git-конфликт на `.jsonl` — но он явный и восстановимый, не тихая потеря; см. разрешение выше).
- Транскрипты содержат код/логи → репо строго **приватный**.
- iCloud-папка `ClaudeProjects` оставлена как бэкап; удалить после стабилизации.
- `make_recents.py` сортирует Recents по `timestamp` из самих транскриптов (не по `mtime` — тот сбивается при `git pull`); бэкафиллит время и в уже созданных записях.

Связано: [[require-explicit-approval]]. Заменяет прежнюю iCloud-схему.
