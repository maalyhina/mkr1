# What is the difference between REST API and GraphQL, and when should each approach be used?

## Коротка відповідь
REST — це архітектурний стиль, організований навколо ресурсів із використанням стандартних методів HTTP та окремих ендпоінтів для кожного ресурсу [1]. GraphQL — це мова запитів та середовище виконання, яка дозволяє клієнтам запитувати конкретні поля через єдиний ендпоінт за допомогою визначеної схеми [1]. REST підходить для простих CRUD-операцій та кешування на основі HTTP, тоді як GraphQL ідеальний для складних зв'язків даних і клієнтів, яким потрібні різні комбінації полів [1].

## Деталі
| Критерій | REST API | GraphQL |
|---|---|---|
| Архітектура та ендпоінти | Використовує окремі ендпоінти для різних ресурсів (наприклад, `/users`, `/products/1`) [1]. | Зазвичай використовує єдиний ендпоінт для всіх операцій [1]. |
| Вибір даних | Структура відповіді визначається сервером; часто повертає зайві дані (overfetching) або вимагає додаткових запитів (underfetching) [1, 2]. | Клієнт самостійно вказує потрібні поля в запиті, уникаючи зайвих даних [1]. |
| Методи та операції | Використовує стандартні методи HTTP (GET, POST, PUT, PATCH, DELETE) [1]. | Використовує запити (queries), мутації (mutations) та підписки (subscriptions) [1]. |
| Кешування | Природно працює з HTTP-кешуванням та заголовками кешу [1]. | Часто використовує клієнтське кешування; HTTP-кешування потребує додаткового конфігурування [1]. |
| Коли використовувати | Ресурсні API, прості CRUD-операції, додатки, що виграють від стандартної семантики HTTP [1]. | Додатки зі складними зв'язками даних або кілька клієнтів із різними потребами в полях [1]. |

## Ризики та підводні камені
* Складність кешування: на відміну від REST, кешування відповідей GraphQL на рівні HTTP вимагає додаткового налаштування [1].
* Надмірне навантаження на сервер (N+1 query problem): складні вкладені запити в GraphQL можуть призвести до неефективного виконання запитів до бази даних, якщо резолвери (resolvers) налаштовані неправильно.
* Управління небезпечними змінами (breaking changes): хоча GraphQL дозволяє додавати нові поля та позначати старі як застарілі, критичні зміни в схемі вимагають ретельного управління [1].
* *Залежність від версії бібліотеки/специфікації:* специфікація GraphQL визначає базову поведінку, але конкретні можливості транспортного рівня (наприклад, підписки через WebSockets), інструменти кешування та методи оптимізації безпосередньо залежать від версій використовуваних серверних і клієнтських бібліотек.

## Джерела
- [1] [REST vs GraphQL - GeeksforGeeks](https://www.geeksforgeeks.org/graphql/graphql-vs-rest-which-is-better-for-apis/)
- [2] [GraphQL vs REST API - Difference Between API Design ...GraphQL vs. REST API: What’s the difference? - IBMGraphQL vs REST: Key differences and how to choose - VercelGraphQL vs REST - BaeldungGraphQL vs REST: Key Differences & When to Use EachGraphQL vs REST | Postman Blog](https://aws.amazon.com/compare/the-difference-between-graphql-and-rest/)
- [3] [GraphQL vs. REST API: What’s the difference? - IBM](https://www.ibm.com/think/topics/graphql-vs-rest-api)
- [4] [GraphQL vs REST: Key differences and how to choose - Vercel](https://vercel.com/i/graphql-vs-rest)
- [5] [GraphQL vs REST - Baeldung](https://www.baeldung.com/graphql-vs-rest) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [GraphQL vs REST: Key Differences & When to Use Each](https://wso2.com/api-platform/learn/graphql-vs-rest/) *(лише уривок із пошуку, сторінку не прочитано)*
