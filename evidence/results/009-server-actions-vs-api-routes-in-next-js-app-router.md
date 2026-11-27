# Server Actions vs API routes in Next.js App Router: when to use which?

## Коротка відповідь
Server Actions ідеально підходять для обробки надсилань форм, мутацій даних та взаємодії з інтерфейсом всередині додатку Next.js [1, 4]. API Routes (Route Handlers) слід використовувати для створення публічних REST-ендпоінтів, вебхуків та інтеграцій із зовнішніми сервісами [1, 3, 4].

## Деталі

| Критерій | Server Actions | API Routes (Route Handlers) |
| :--- | :--- | :--- |
| **Призначення** | Мутації даних, форми, логіка, прив'язана до UI [1, 4] | Стабільні HTTP-ендпоінти, вебхуки, зовнішні клієнти [1, 4] |
| **Доступність** | Тільки зсередини додатку Next.js [1] | Будь-які зовнішні сервіси та клієнти [1, 4] |
| **Формат виклику** | Напряму з компонентів або через атрибут `action` [1, 2] | Через HTTP-запити (`fetch` з методами GET, POST тощо) [1, 2] |

1. Визначте призначення логіки: якщо це взаємодія з формами або зміна стану даних усередині UI — використовуйте Server Actions [1, 4].
2. Додайте директиву `'use server'` на початку файлу або функції для створення Server Action [1, 4].
3. Якщо потрібен публічний протокол для зовнішніх споживачів або вебхуків — створіть файл маршруту (наприклад, `route.js` або `route.ts`) у папці `app/api` [1, 4].
4. Експортуйте відповідні HTTP-методи (`GET`, `POST` тощо) з файлу маршруту для обробки запитів через стандартні об'єкти `NextResponse` [1, 4].

## Ризики та підводні камені
* **Експериментальна / змінні версії (залежить від версії бібліотеки):** В окремих ранніх або проміжних релізах Next.js Server Actions згадувалися як експериментальна функція, чиє стабільне API могло змінюватися [3].
* **Обмеження доступу:** Server Actions не можуть викликатися сторонніми сервісами, оскільки вони не є повноцінними REST-ендпоінтами загального призначення [1].
* **Проблеми продуктивності API Routes:** Використання традиційних серверних функцій (API Routes / Serverless functions) може стикатися із затримками «холодного старту» (*cold start latency*) та обмеженнями часу виконання (*execution time*) [3].

## Джерела
- [1] [Next.js Server Actions vs API Routes: Don’t Build Your App ...](https://dev.to/myogeshchavan97/nextjs-server-actions-vs-api-routes-dont-build-your-app-until-you-read-this-4kb9)
- [2] [Next.js API Routes vs Server Actions — When to Use Which](https://prateeksha.com/blog/nextjs-api-routes-vs-server-actions)
- [3] [Next.js API Routes vs. Server Actions: Which One to Use and ...](https://medium.com/@shavaizali159/next-js-api-routes-vs-server-actions-which-one-to-use-and-why-809f09d5069b)
- [4] [Server Actions vs. API Routes in Next.js | John Kavanagh](https://johnkavanagh.co.uk/articles/when-to-use-server-actions-vs-api-routes-in-nextjs/)
- [5] [Server Actions vs API Routes in Next.js: the rules I actually use](https://www.pean.dev/blog/server-actions-vs-api-routes-in-nextjs-rules-i-use) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [Next.js Server Actions vs API Routes | Prateeksha Web Design](https://prateeksha.com/blog/forms-mutations-nextjs-app-router-server-actions-vs-api-routes) *(лише уривок із пошуку, сторінку не прочитано)*
