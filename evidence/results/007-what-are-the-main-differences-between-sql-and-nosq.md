# What are the main differences between SQL and NoSQL databases?

## Коротка відповідь
SQL та NoSQL — це два основні типи баз даних, які відрізняються структурою зберігання даних, схемою та масштабованістю [1]. SQL використовує реляційні моделі з фіксованою схемою і таблицями, тоді як NoSQL застосовує нереляційні моделі з гнучкою чи динамічною схемою для неструктурованих даних [1, 2, 3].

## Деталі
| Характеристика | SQL (Реляційні) | NoSQL (Нереляційні) |
|---|---|---|
| Структура даних | Дані зберігаються у таблицях з рядками та стовпцями [1]. | Дані зберігаються як документи, пари ключ-значення, графи або стовпці [1]. |
| Схема | Жорстка, заздалегідь визначена фіксована схема [1, 3]. | Гнучка та динамічна схема [1, 3]. |
| Масштабування | Масштабується вертикально (збільшення потужності сервера) [1]. | Масштабується горизонтально (додавання нових серверів) [1]. |
| Транзакції та зв'язки | Дотримуються принципів ACID, підтримують складні JOIN [1]. | Зазвичай слідують моделі BASE, уникають складних JOIN [1]. |
| Приклади використання | Банківські системи, ERP, CRM [1]. | Соцмережі, Big Data, IoT, реальний час [1]. |

## Ризики та підводні камені
* Проблеми при горизонтальному масштабуванні SQL: хоча SQL-бази найчастіше масштабують вертикально, вони можуть масштабуватися горизонтально через шардинг або партиціювання, проте ця функція підтримується гірше [2].
* Залежності від конкретної бібліотеки, версії чи рушія у наданих джерелах не задекларовано (усі відмінності стосуються архітектурних концепцій баз даних загалом, а не конкретних версій програмного забезпечення).

## Джерела
- [1] [SQL vs. NoSQL - GeeksforGeeks](https://www.geeksforgeeks.org/sql/difference-between-sql-and-nosql/)
- [2] [SQL vs. NoSQL Databases: What’s the difference? - IBM](https://www.ibm.com/think/topics/sql-vs-nosql)
- [3] [Relational Database vs NoSQL - GeeksforGeeks](https://www.geeksforgeeks.org/dbms/difference-between-relational-database-and-nosql/)
- [4] [NoSQL Vs SQL Databases | MongoDB](https://www.mongodb.com/resources/basics/databases/nosql-explained/nosql-vs-sql)
- [5] [NoSQL vs. SQL: The Differences Explained + When to Use Each](https://www.coursera.org/articles/nosql-vs-sql) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [SQL vs NoSQL Databases: Key Differences and Practical ...](https://www.datacamp.com/blog/sql-vs-nosql-databases) *(лише уривок із пошуку, сторінку не прочитано)*
