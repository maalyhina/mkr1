# Prisma 7 vs Prisma 6: breaking changes and should I upgrade a Next.js project?

## Коротка відповідь
Prisma 7 пропонує архітектурний перехід на чистий TypeScript і WASM замість окремого Rust-рушія, що суттєво зменшує розмір бандла та покращує підтримку edge-середовищ [3], [4]. Оновлювати Next.js проєкт варто, якщо вам потрібні швидкі холодні старти, робота на Edge або типизований SQL, проте слід бути готовим до зламуючих змін (breaking changes) в імпортах та конфігурації [1], [3].

## Деталі
1. **Оновіть пакети** `prisma` та `@prisma/client` до версії 7, а також налаштуйте мінімальні системні вимоги (Node.js від 20.19.0, TypeScript від 5.4.0) [1].
2. **Змініть генератор у схемі (`schema.prisma`):** замініть старий провайдер на новий `prisma-client` та обов'язково вкажіть шлях виводу у полі `output` (наприклад, у папку `./generated/prisma`) [1], [4].
3. **Оновіть імпорти в коді Next.js:** оскільки клієнт більше не генерується всередині `node_modules` за замовчуванням, змініть шлях імпорту (наприклад, на `@/generated/prisma/client`) [1], [3].
4. **Підключіть драйвер-адаптери:** для всіх баз даних тепер обов'язково потрібно встановлювати та передавати відповідний драйвер-адаптер (наприклад, `@prisma/adapter-pg` для PostgreSQL) під час ініціалізації `PrismaClient` [1].
5. **Налаштуйте конфігурацію та з'єднання:** перенесіть параметри на кшталт `url` та `directUrl` до файлу `prisma.config.ts`, якщо це необхідно, та перевірте налаштування пулу з'єднань, оскільки їх поведінка змінилася порівняно з дефолтами v6 [1].

## Ризики та підводні камені
* **Відсутність підтримки MongoDB:** якщо ваш проєкт використовує MongoDB, оновлюватися на Prisma 7 не можна (підтримка з'явилася лише в ранньому доступі з версії 8) [1].
* **Зміна шляху генератора (generator path footgun):** найчастіша помилка при міграції — невідповідність нових шляхів імпорту згенерованого клієнта в репозиторії [3].
* **Зміна таймаутів пулу з'єднань:** нові драйвер-адаптери використовують параметри базового драйвера Node.js, що може призвести до неочікуваних таймаутів під навантаженням (наприклад, у драйвера `pg` таймаут за замовчуванням відсутній, тоді як у v6 було 5 секунд) [1].
* **Вимоги до модулів:** Prisma 7 постачається як ES-модуль, тому у `package.json` потрібно встановити `type: "module"`, а також відповідно налаштувати `tsconfig.json` [1].
* *Залежність від версії бібліотеки:* залежно від точного патч-релізу v7 можуть з'являтися додаткові інструменти чи виправлення (наприклад, покращення продуктивності у версії 7.3.0) [2], а також нюанси роботи з `pnpm` (наприклад, дозвіл виконання скриптів збірки для `better-sqlite3`) [1].

## Джерела
- [1] [Upgrade to Prisma ORM 7](https://www.prisma.io/docs/guides/upgrade-prisma-orm/v7)
- [2] [Prisma 7 AMA: Clearing Up the Why Behind the Changes](https://www.prisma.io/blog/prisma-7-ama-clearing-up-the-why-behind-the-changes)
- [3] [Prisma 7 Migration Playbook: Typed SQL, Rust Deprecation](https://www.digitalapplied.com/blog/prisma-7-migration-playbook-from-6-typed-sql-rust-deprecation)
- [4] [What's New in Prisma 7 and How to Upgrade | Ayush Sharma](https://aysh.me/blogs/prisma-7)
- [5] [Prisma v6 → v7 migration guide: safely crossing Rust-free ...](https://tomodahinata.com/en/blog/prisma-orm-v6-to-v7-migration-guide) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [prisma-upgrade-v7 — prisma/skills](https://www.skills.sh/prisma/skills/prisma-upgrade-v7) *(лише уривок із пошуку, сторінку не прочитано)*
