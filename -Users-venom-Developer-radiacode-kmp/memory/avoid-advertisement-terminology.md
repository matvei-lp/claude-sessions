---
name: avoid-advertisement-terminology
description: BLE-перенос — не злоупотреблять словом «реклама»/advertisement в неймингах и описаниях
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ffab373d-a29f-4a9f-a990-fa2e9b3c2349
---

При портировании BLE избегать слова «реклама» / «advertisement» в именах типов и функций и в описаниях для пользователя. Предпочитать нейтральное: «результат сканирования», «найденное устройство», «BLE-имя».

**Why:** пользователь прямо одёрнул — «Хватит всё называть рекламой!».

**How to apply:** парсер находки скана — это `RadiaCodeDiscovery.parse(...)` (фабрика на core-модели), НЕ `RadiaCodeAdvertisement`/`RadiaCodeScanRecord`. Параметры `name`/`localName` оставлять — это технические поля Kable `Advertisement`, имена нейтральны. Тема всплывёт снова на connect-слое. См. [[kmp-shared-vm-stack]].
