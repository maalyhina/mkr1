# Tailwind CSS v4: what changed in configuration compared to v3?

## Коротка відповідь
У Tailwind CSS v4 основні зміни в конфігурації полягають у переході від файлу JavaScript (`tailwind.config.js`) до CSS-орієнтованого підходу з використанням директиви `@theme` [2, 3]. Також було спрощено імпорт, видалено необхідність вручну налаштовувати шляхи до шаблонів (content array) та впроваджено нативні CSS-змінні для управління темою [1, 3, 4].

## Деталі
Порівняння конфігурації у версіях v3 та v4:

| Аспект конфігурації | Tailwind CSS v3 | Tailwind CSS v4 |
|---|---|---|
| Основний файл налаштувань | JavaScript-файл (`tailwind.config.js`) [2, 3] | CSS-файл із директивою `@theme` [2, 3] |
| Підключення у стилях | Три директиви (`@tailwind base; @tailwind components; @tailwind utilities;`) [1, 3] | Один імпорт (`@import "tailwindcss";`) [1, 3] |
| Шляхи до шаблонів (Content) | Налаштовувалися вручну у конфіг-файлі [3, 4] | Визначаються автоматично (на основі евристики та `.gitignore`) [3, 4] |
| Значення теми | Компілюються у статичні значення [2] | Експортуються як нативні CSS-змінні (доступні в рантаймі) [2, 3] |

## Ризики та підводні камені
* **Зміна синтаксису кастомізації:** Перенесення значень кольорів, шрифтів та інших параметрів у CSS-змінні всередині блоку `@theme` вимагає переписування старої JavaScript-конфігурації [3, 4].
* **Проблеми зі старішими браузерами:** v4 використовує сучасні можливості платформи (такі як `@property` та `color-mix()`), тому вона не працюватиме в застарілих браузерах, на відміну від v3 [1, 3].
* **Залежність від версії бібліотеки та інструментів зйомки білду:** У v4 пакет PostCSS винесено в окремий модуль (`@tailwindcss/postcss`), а також змінено пакети для CLI та Vite, що потребує оновлення залежностей і конфігурацій збирача проєктів [1, 3, 4]. Автоматичний інструмент міграції (`npx @tailwindcss/upgrade`) вимагає Node.js 20 або вище [1].

## Джерела
- [1] [Upgrade guide - Getting started - Tailwind CSS](https://tailwindcss.com/docs/upgrade-guide)
- [2] [Tailwind CSS v4 vs v3 - Complete Comparison (2026) | Frontend ...](https://frontend-hero.com/tailwind-v4-vs-v3)
- [3] [Tailwind 4 vs Tailwind 3: Key Differences and Improvements ...](https://staticmania.com/blog/tailwind-v4-vs-v3-comparison)
- [4] [Migrating from Tailwind CSS v3 to v4: A Complete Developer's ...](https://dev.to/elechipro/migrating-from-tailwind-css-v3-to-v4-a-complete-developers-guide-cjd)
- [5] [Tailwind CSS v4.0](https://tailwindcss.com/blog/tailwindcss-v4) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [Migration Guide: Tailwind CSS v3 to v4 - DEV Community](https://dev.to/ippatev/migration-guide-tailwind-css-v3-to-v4-f5h) *(лише уривок із пошуку, сторінку не прочитано)*
