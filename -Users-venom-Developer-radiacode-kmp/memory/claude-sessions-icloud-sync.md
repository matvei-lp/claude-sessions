---
name: claude-sessions-icloud-sync
description: ~/.claude/projects is a symlink into iCloud; CLI sessions shared across Macs (venom ↔ mkozin) via alias symlinks
metadata: 
  node_type: memory
  type: project
  originSessionId: 98f573b0-c435-4b42-bcc2-47f75f4802e9
---

CLI-сессии Claude Code шарятся между двумя маками Матвея через iCloud Drive (настроено 2026-06-18).

Устройство:
- `~/.claude/projects` — **симлинк** на `~/Library/Mobile Documents/com~apple~CloudDocs/ClaudeProjects/projects` (реальный стор в iCloud, ~74 МБ).
- Реальные папки сессий именуются по пути проекта мака venom: `-Users-venom-Developer-radiacode-*`.
- Второй мак — username **mkozin**, путь `/Users/mkozin/Developer/...`. Claude там ищет папку `-Users-mkozin-...`, поэтому в сторе лежат **относительные симлинки-алиасы** `-Users-mkozin-… -> -Users-venom-…`.

Обслуживание: после создания НОВОГО проекта на venom-маке нужно досоздать mkozin-алиас:
```bash
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeProjects"
for p in "$ICLOUD/projects"/-Users-venom-*; do b=$(basename "$p"); a="${b/-Users-venom-/-Users-mkozin-}"; [ -e "$ICLOUD/projects/$a" ] || ln -s -- "$b" "$ICLOUD/projects/$a"; done
```

Ограничения:
- **Не запускать `claude` на обоих маках одновременно** в этом сторе — iCloud мержит «кто последний записал», параллельная запись бьёт `.jsonl`.
- Оба мака должны быть под **одним Apple ID** (иначе iCloud не синкает папку).
- Память (`memory/`) лежит внутри папок проектов → синкается вместе с сессиями.

## Recents-панель десктоп-приложения (отдельная от iCloud-синка)

Список «recents» слева в десктоп-приложении НЕ читается из `~/.claude/projects/*.jsonl`. Он строится при старте приложения из записей-обёрток:
`~/Library/Application Support/Claude/claude-code-sessions/<workspaceA>/<workspaceB>/local_<uuid>.json`.

Каждая запись — лёгкий json: `sessionId` (local_<uuid>), `cliSessionId` (→ `.jsonl`), `cwd`, `title`, таймстемпы (мс), `isArchived`; плюс болванка `remoteMcpServersConfig`. Транскрипта внутри нет — он тянется из `.jsonl` по `cliSessionId`. CLI-сессии из терминала такой записи не получают → в recents не видны.

Чтобы CLI-сессия попала в recents: создать `local_*.json` (склонировать существующую запись, подменить `sessionId`/`cliSessionId`/`cwd`/`title`/таймстемпы), положить в ту же workspace-папку и **перезапустить приложение** (`Cmd+Q` → открыть) — список читается только на старте, вживую файлы не перечитываются. Проверено 2026-06-18: сработало, все 42 сессии завелись.

Важно: этот стор **локальный для мака, НЕ в iCloud**. На маке mkozin recents надо заполнять отдельно (там `cwd` будет `/Users/mkozin/...`, нормализация не нужна). Бэкап перед правкой: `cp -R claude-code-sessions claude-code-sessions.bak-<ts>`.

Связано: [[require-explicit-approval]]
