---
name: project_kmp_migration
description: Проект переезжает на KMP; структура Jira-проекта RMP и граница Core vs платформы.
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e6d2172-8ecd-4f23-8c9e-c8749136721e
---

Вся дальнейшая работа над radiacode-ios идёт через **KMP (Kotlin Multiplatform)** (заявлено 2026-06-02). Цель — общая бизнес-логика для iOS/Android/Web.

**Jira-проект `RMP` (Radiacode MP)**, cloudId `8a7ee723-e1df-4755-a83f-c4063369fa84`. Иерархия 4 уровня: Инициатива → Эпик → Задача/История → Подзадача.

Инициативы (верхний уровень):
- **RMP-1 `[Core] Shared Business Logic`** (Igor) — commonMain на Kotlin: BLE-протокол, расчёты, модели, persistence (SQLDelight), Ktor, Koin. Target Q2 2026 – Q1 2027.
- **RMP-2 `[Android]`** (Ivan), **RMP-3 `[iOS]`** (пользователь Matvei), **RMP-4 `[Web]`** (Ivan, Kotlin/JS).
- **RMP-5 `[Core/Infra] Build & Gradle`** — первый Эпик под RMP-1 (монорепо `shared/ androidApp/ iosApp/ webApp/`, XCFramework).

**Граница:** общая логика → Core/RMP-1 (commonMain); UI (нативный SwiftUI) + платформенный код (BLE transport на CoreBluetooth, SQL driver, expect-actual) → инициативы платформ. По BLE: codec/reassembly/queue/state machine + `expect BleScanner/BleCentral/BleConnection` → common; `CBCentralManager`/`CBPeripheral` → iosMain actual.

**Why:** определяет, куда вешать задачи и код в дальнейшей работе.
**How to apply:** новые KMP-задачи — под нужную инициативу RMP; общую логику класть в Core/commonMain, платформенное — в actual соответствующей платформы. Координаты Jira — [[reference_jira_bitbucket]].

**Репозиторий KMP — на GitHub** (в отличие от iOS, который на Bitbucket): `git@github.com:Radiacode/radiacode-kmp.git` — монорепо по RMP-5. Склонирован локально в `/Users/mkozin/Developer/radiacode-kmp` (2026-06-02). Ветки `main`/`develop`/`app-init`/`app-init-v2`, на старте — скелет (коммит «init stuff», `.gitignore`/`README.md`/`CLAUDE.md`). **GitHub-личность пользователя — `matvei-lp`** (не путать с Bitbucket-логином `mvkozin`). Доступ к приватному репо — по **SSH-ключу** `~/.ssh/id_ed25519` (ed25519, без пароля, привязан к `matvei-lp`); настроен `~/.ssh/config` с блоком github.com; в Fork выставить Git → SSH Client = System. Fork хранит свои OAuth-учётки в Keychain как generic-password `Fork.<host>.https` / `fork:https://<host>.<account>.{oauth,accesstoken}` — отдельно от git CLI (osxkeychain ищет internet-password по хосту).
