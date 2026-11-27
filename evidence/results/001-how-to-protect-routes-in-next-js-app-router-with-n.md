# How to protect routes in Next.js App Router with NextAuth v5 middleware?

## Коротка відповідь
Для захисту маршрутів у Next.js App Router за допомогою NextAuth v5 (Auth.js) використовується універсальна функція `auth`, яку можна експортувати з головного файлу конфігурації у файл `middleware.ts` на рівні кореню проєкту [4]. Завдяки цьому middleware виконується на «edge»-сервері до рендерингу сторінки, перевіряючи наявність сесії через `req.auth` та перенаправляючи неавторизованих користувачів [2, 4].

## Деталі
1. **Створіть або оновіть файл конфігурації NextAuth (наприклад, `auth.ts` у корені проєкту)**, де налаштуйте провайдерів та експортуйте об'єкт `auth` [4].
2. **Створіть маршрут для обробки запитів аутентифікації** у файлі `app/api/auth/[...nextauth]/route.ts`, експортувавши `GET` та `POST` обробники з вашої конфігурації [4].
3. **Створіть файл `middleware.ts` на рівні кореню проєкту** (поряд із папкою `app`) для централізованої перевірки прав доступу [2, 4].
4. **Налаштуйте логіку перевірки та конфігурацію `matcher`** у файлі `middleware.ts`, щоб захистити лише потрібні шляхи (наприклад, `/dashboard/:path*`) [4]:
```typescript
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard')
  
  if (isOnDashboard && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.nextUrl))
  }
  
  return NextResponse.next()
})

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

## Ризики та підводні камені
* **Неправильне налаштування `matcher`:** Застосування занадто широких масок (або запуск на всіх запитах без виключення статичних файлів) може призвести до зайвої затримки (латентності) та виконання коду на статичних ресурсах чи зображеннях [2, 4].
* **Проблеми з контекстом:** У старіших версіях (NextAuth v4) використовувався специфічний middleware, який вимагав стратегію сесій виключно типу `jwt` [1] і не підтримувався безпосередньо в такому ж вигляді для App Router, як v5 [4].
* **Архітектурні особливості версій (Залежить від версії Next.js):** У новіших версіях Next.js (Next.js 16+) файл `middleware.ts` може вимагати перейменування на `proxy.ts`, а функція `middleware` — на `proxy` (докладніше див. офіційну міграцію або залежно від актуальної мінорної версії фреймворку) [2].

## Джерела
- [1] [Securing pages and API routes | NextAuth.js](https://next-auth.js.org/tutorials/securing-pages-and-api-routes)
- [2] [Next.js Middleware Authentication: Protect Routes in App Router](https://www.authgear.com/post/nextjs-middleware-authentication/)
- [3] [How to implement protected route with next-auth v5 and Next ...](https://stackoverflow.com/questions/79306975/how-to-implement-protected-route-with-next-auth-v5-and-next-js-14-15) *(лише уривок із пошуку, сторінку не прочитано)*
- [4] [I am Raghuveer | Authentication in Next.js App Router ...](https://www.iamraghuveer.com/posts/nextjs-authentication-nextauth-v5/)
- [5] [App Router: Adding Authentication | Next.js](https://nextjs.org/learn/dashboard-app/adding-authentication) *(лише уривок із пошуку, сторінку не прочитано)*
- [6] [Next.js Protected Routes: Auth Middleware and JWT Guide](https://focusreactive.com/blog/nextjs-protected-routes-middleware-jwt/) *(лише уривок із пошуку, сторінку не прочитано)*
