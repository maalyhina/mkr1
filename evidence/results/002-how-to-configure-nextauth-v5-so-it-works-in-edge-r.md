# How to configure NextAuth v5 so it works in Edge Runtime with Prisma?

## Коротка відповідь
Щоб налаштувати NextAuth v5 (Auth.js) для роботи в середовищі Edge Runtime із використанням Prisma, необхідно застосувати розділену конфігурацію (`split architecture`). Оскільки Prisma та бібліотеки хешування базуються на Node.js API, які не підтримуються Edge, конфігурацію розбивають на Edge-сумісну частину (`auth.config.ts`) та основний файл з адаптером і провайдерами (`auth.ts`) [3].

## Деталі
1. **Створіть Edge-сумісний файл конфігурації (`auth.config.ts`)**: Визначте провайдерів, параметри сторінок та колбеки (callbacks), які не використовують Node.js-модулі чи Prisma безпосередньо [3, 4].
2. **Створіть основний файл конфігурації (`auth.ts`)**: Імпортуйте туди `authConfig`, підключіть адаптер Prisma та експортуйте об'єкти `handlers`, `auth`, `signIn` і `signOut` [1, 4].
3. **Налаштуйте Route Handler**: Експортуйте `GET` та `POST` обробники з файлу маршруту API (наприклад, `app/api/auth/[...nextauth]/route.ts`), використовуючи створені handlers [1, 3, 4].
4. **Налаштуйте Middleware для Edge Runtime**: Використовуйте `auth` експортований з основної конфігурації (або через middleware-обгортку), щоб захистити маршрути на рівні Edge [3, 4].

## Ризики та підводні камені
* **Несумісність Node.js API з Edge**: Пряме використання Prisma Client або пакетів для хешування паролів (наприклад, `bcrypt`) у файлах, що виконуються на Edge Runtime, призведе до помилок збирання чи виконання [3].
* **Роздільна архітектура конфігурації**: Помилкове об'єднання бази даних, адаптера та логіки бази в один файл разом із конфігурацією middleware завадить роботі в Edge Runtime [3].
* **Залежність від версії бібліотеки**: 
  * У NextAuth v5 (beta) змінилася структура експортів порівняно з v4: відсутній файл `[...nextauth].js` у папці `pages/api`, натомість використовується App Router та єдиний виклик `NextAuth()` [1, 3].
  * Конкретні назви полів у параметрах провайдерів (наприклад, `tenantId` замість `tenantId` в об'єкті params для Microsoft) можуть залежати від точної мінорної чи бета-версії пакета [4].

## Джерела
- [1] [Auth.js v5 with Next.js 16: The Complete Authentication Guide ...](https://dev.to/huangyongshan46a11y/authjs-v5-with-nextjs-16-the-complete-authentication-guide-2026-2lg)
- [2] [Build Modern Stack with Nextjs and NextAuth 5.x with Prisma](https://dev.to/inditechcoder/build-modern-stack-with-nextjs-and-nextauth-5x-with-prisma-7fi)
- [3] [Mastering Auth.js v5 (NextAuth) in Next.js 15 App Router ...](https://www.snippetcrafted.com/blog/authjs-v5-nextjs-15-authentication-guide)
- [4] [Simplifying Authentication in Next.js with NextAuth v5 ...](https://medium.com/@ricardo.jucrist/simplifying-authentication-in-next-js-with-nextauth-v5-microsoft-and-prisma-a40f12b5227c)
- [5] [How to use Prisma ORM and Prisma Postgres with Auth.js and ...](https://www.prisma.io/docs/guides/authentication/authjs/nextjs) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [A Next.js Prisma + Auth.js (NextAuth) v5 Starter](https://eamongordon.com/blog/next-prisma-auth-starter/) *(лише уривок із пошуку, сторінку не прочитано)*
