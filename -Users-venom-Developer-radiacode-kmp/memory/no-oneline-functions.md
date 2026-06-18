---
name: no-oneline-functions
description: Не писать Kotlin-функции в одну строку — тело разворачивать в блок на отдельных строках
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6ebeb5ea-e89a-4b9d-8153-1d3821f98048
---

Матвей не любит функции, сжатые в одну строку — ни `fun x() { stmt }`, ни expression-body `fun x() = expr`, когда всё на одной строке. Тело функции писать многострочно, в блоке:

```kotlin
fun connect(discovery: RadiaCodeDiscovery) {
    target.value = Target.Connect(discovery)
}
```
а не `fun connect(discovery) { target.value = ... }` и не `... = ...` одной строкой.

**Why:** читаемость и единый стиль кодовой базы radiacode-kmp.

**How to apply:** в Kotlin-коде методы давать блочным телом с операторами на отдельных строках. Простые `val`-свойства/геттеры — это не функции, их разворачивать не обязательно. Относится и к показу кода в чате, и к записи в файлы. Связано с [[require-explicit-approval]] (его правки стиля держим).
