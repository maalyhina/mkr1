# How to connect Prisma to Neon PostgreSQL in Next.js and avoid connection limit problems?

## Коротка відповідь
Щоб підключити Prisma до Neon PostgreSQL у Next.js та уникнути проблем із лімітами з'єднань, використовуйте вбудований пул з'єднань Neon (додавши `-pooler` до хоста) або Prisma Accelerate [2, 3]. Також важливо реалізувати патерн Singleton для `PrismaClient`, щоб запобігти створенню зайвих з'єднань під час гарячого перезавантаження (hot reload) у середовищі розробки [4].

## Деталі
1. Налаштуйте два рядки підключення у файлі `.env`: рядок із пуллом з'єднань (`-pooler` у назві хоста) для роботи додатку та прямий рядок (direct URL) для міграцій [1, 2].
2. Налаштуйте конфігурацію Prisma (`prisma.config.ts`), вказавши пряме підключення для інструментів CLI [1, 2].
3. Використовуйте драйвер-адаптер Neon (`@prisma/adapter-neon`) та ініціалізуйте `PrismaClient` за допомогоюpooled-з’єднання під час виконання програми [1, 2].
4. Застосуйте патерн Singleton для `PrismaClient` через `globalThis`, щоб уникнути вичерпування пулу з'єднань через гарячі перезавантаження у Next.js [4]:
   ```typescript
   import { PrismaClient } from '@prisma/client';

   const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined };

   export const prisma = globalForPrisma.prisma ?? new PrismaClient();

   if (process.env.NODE_ENV !== 'production') {
     globalForPrisma.prisma = prisma;
   }
   ```
5. Обмежте кількість з'єднань у параметрах рядка підключення відповідно до лімітів вашого плану Neon (наприклад, `connection_limit=10` для безплатного тарифу) [4].

## Ризики та підводні камені
* **Версії Prisma:** Інструкції відрізняються залежно від версії. Наприклад, для Prisma 7 конфігурація виноситься у файл `prisma.config.ts`, а пакети обов'язково закріплюються за мажорною версією (наприклад, `@7`), оскількимістить відмінності від Prisma 6 та ранніх версій [1, 2, 3].
* **Холодні старти (Cold starts):** Neon переводить обчислювальний модуль (compute) в режим очікування (idle) після 5 хвилин неактивності, що може викликати тайм-аути підключення [2]. Залежно від версії та конфігурації, це вимагає налаштування параметра `connect_timeout` у рядку підключення [2, 4].
* **Розробка проти продакшну:** Створення нового екземпляра `PrismaClient` на кожній сторінці або під час кожного hot reload у Next.js швидко вичерпує ліміт з'єднань бази даних, якщо не використовувати Singleton [4].

## Джерела
- [1] [Connect from Prisma to Neon - Neon Docs](https://neon.com/docs/guides/prisma)
- [2] [Neon (Prisma ORM v6) | Prisma Documentation](https://www.prisma.io/docs/orm/v6/overview/databases/neon)
- [3] [Set up PostgreSQL on Neon with Prisma Accelerate's Connection ...](https://www.prisma.io/docs/guides/v7/integrations/neon-accelerate)
- [4] [Optimizing Connection Pools with PrismaClient Singleton ...](https://dev.to/_877737de2d34ff8c6265/optimizing-connection-pools-with-prismaclient-singleton-pattern-in-nextjs-3emf)
- [5] [Connect a Next.js application to Neon - Neon Docs](https://neon.com/docs/guides/nextjs) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [How to Set Up Prisma with PostgreSQL in Next.js (Supabase ...](https://zerodrag.cloud/blog/prisma-postgresql-nextjs-setup) *(лише уривок із пошуку, сторінку не прочитано)*
