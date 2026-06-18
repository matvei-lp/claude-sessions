# @ViewBuilder — хранимое свойство, не замыкание

Всегда использовать статический подход: `@ViewBuilder let content: Content` как хранимое свойство.
Явный `init` писать не нужно — Swift генерирует его автоматически с `@ViewBuilder` параметром.

```swift
// ✅ Правильно — вычисляется один раз, хранится как значение
struct MyView<Content: View>: View {
    let title: String
    @ViewBuilder let content: Content

    var body: some View {
        VStack {
            Text(title)
            content
        }
    }
}

// Использование
MyView(title: "Hello") {
    Text("World")
}
```

```swift
// ❌ Неправильно — замыкание вызывается при каждом перестроении вью
struct MyView<Content: View>: View {
    @ViewBuilder let content: () -> Content

    var body: some View {
        content() // лишние накладные расходы
    }
}
```

Источник: https://erezhod.com/blog/mastering-swiftui-viewbuilder/
