# DjangoREST — LMS API

REST API для учебной платформы на Django REST Framework.

Проект предоставляет API для управления пользователями, курсами, уроками, подписками и платежами. Реализованы JWT-аутентификация, разграничение прав пользователей и модераторов, пагинация, фильтрация, документация API и интеграция со Stripe Checkout.

## Стек

* Python 3.14
* Django 6.x
* Django REST Framework
* PostgreSQL
* Poetry
* Simple JWT
* django-filter
* drf-yasg
* Stripe API
* Pillow
* python-dotenv
* pytest / Django Test Framework
* coverage

## Возможности

### Пользователи

* регистрация пользователей;
* авторизация по email и паролю;
* JWT-аутентификация;
* получение и обновление JWT-токена;
* редактирование профиля пользователя;
* аватар, телефон и город.

### Курсы

* создание курса;
* просмотр списка курсов;
* просмотр отдельного курса;
* изменение курса;
* удаление курса;
* привязка курса к пользователю-владельцу;
* автоматический подсчёт количества уроков;
* отображение статуса подписки пользователя на курс.

### Уроки

* создание уроков;
* просмотр списка уроков;
* просмотр отдельного урока;
* изменение и удаление уроков;
* привязка урока к владельцу;
* урок можно создавать только в собственном курсе;
* проверка ссылки на видео — разрешены только YouTube-ссылки.

### Подписки

Для каждого пользователя и курса может существовать только одна подписка.

Доступны операции:

* подписка на курс;
* повторная подписка без создания дубликата;
* отписка от курса;
* проверка текущего статуса подписки через `is_subscribed`.

### Платежи

Реализована интеграция со Stripe в тестовом режиме.

При создании платежа:

1. создаётся локальный объект `Payment`;
2. в Stripe создаётся Product;
3. создаётся Price;
4. создаётся Checkout Session;
5. ссылка на оплату сохраняется в `payment_url`;
6. ID Stripe-сессии сохраняется в `stripe_session_id`.

Стоимость передаётся в Stripe в минимальных единицах валюты: например, `1500.00 ₽` преобразуется в `150000`.

### Пагинация

Для курсов и уроков используется собственный класс `LMSPagination`.

По умолчанию:

* размер страницы — 2 объекта;
* параметр изменения размера страницы — `page_size`;
* максимальный размер страницы — 10 объектов.

Пример:

```text
/api/courses/?page_size=5
```

### Фильтрация платежей

Платежи можно фильтровать по:

* курсу;
* уроку;
* способу оплаты.

Пример:

```text
/api/payments/?paid_course=1
```

Также доступна сортировка по дате платежа.

### Права доступа

Используется разграничение прав между обычными пользователями и модераторами.

Обычный пользователь:

* работает со своими курсами и уроками;
* может создавать собственные курсы;
* может создавать уроки только в собственных курсах;
* может изменять и удалять собственные объекты.

Модератор:

* может просматривать курсы и уроки;
* может изменять существующие курсы и уроки;
* не может создавать и удалять курсы или уроки.

Права реализованы через собственные permission-классы `IsModerator` и `IsOwner`.

---

# Структура проекта

```text
DjangoREST/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── lms/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── paginators.py
│   ├── validators.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── users/
│   ├── migrations/
│   ├── fixtures/
│   ├── services/
│   │   └── stripe_service.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── manage.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

# Установка

## 1. Клонирование репозитория

```bash
git clone https://github.com/Sotocs/DjangoREST.git
cd DjangoREST
```

## 2. Установка зависимостей

Проект использует Poetry.

```bash
poetry install
```

Активировать виртуальное окружение:

```bash
poetry shell
```

Либо выполнять команды непосредственно через Poetry:

```bash
poetry run python manage.py ...
```

## 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта.

Пример:

```env
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
```

Секретный ключ Stripe должен быть тестовым и начинаться с:

```text
sk_test_
```

Не добавляйте `.env` в Git.

---

# PostgreSQL

Проект использует PostgreSQL.

Необходимо создать базу данных и указать параметры подключения в настройках Django.

Пример конфигурации:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "lms_db",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

После настройки базы примените миграции:

```bash
poetry run python manage.py migrate
```

---

# Создание суперпользователя

```bash
poetry run python manage.py createsuperuser
```

После создания пользователя можно открыть Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# Запуск проекта

```bash
poetry run python manage.py runserver
```

API будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

---

# Аутентификация

Проект использует JWT.

## Получение токена

```http
POST /api/token/
```

Тело запроса:

```json
{
    "email": "user@example.com",
    "password": "password"
}
```

Ответ:

```json
{
    "refresh": "refresh_token",
    "access": "access_token"
}
```

## Обновление токена

```http
POST /api/token/refresh/
```

```json
{
    "refresh": "refresh_token"
}
```

Для защищённых запросов необходимо передавать:

```text
Authorization: Bearer <access_token>
```

---

# API

## Users

```text
GET     /api/users/
POST    /api/users/
GET     /api/users/{id}/
PUT     /api/users/{id}/
PATCH   /api/users/{id}/
DELETE  /api/users/{id}/
```

Регистрация пользователя не требует авторизации.

Остальные операции требуют JWT-аутентификации.

---

## Courses

```text
GET     /api/courses/
POST    /api/courses/
GET     /api/courses/{id}/
PUT     /api/courses/{id}/
PATCH   /api/courses/{id}/
DELETE  /api/courses/{id}/
```

Созданный курс автоматически получает текущего пользователя в качестве владельца.

В ответе курса присутствуют:

```json
{
    "count_lessons": 3,
    "is_subscribed": true
}
```

### Подписка на курс

```http
POST /api/courses/{id}/subscribe/
```

### Отписка

```http
DELETE /api/courses/{id}/subscribe/
```

---

## Lessons

```text
GET     /api/lessons/
POST    /api/lessons/
GET     /api/lessons/{id}/
PUT     /api/lessons/{id}/
PATCH   /api/lessons/{id}/
DELETE  /api/lessons/{id}/
```

При создании урока ссылка `video_url` проверяется собственным валидатором.

Разрешены:

```text
https://youtube.com/...
https://www.youtube.com/...
https://youtu.be/...
```

Ссылки на другие видеохостинги отклоняются с HTTP `400`.

---

## Payments

```text
GET     /api/payments/
POST    /api/payments/
GET     /api/payments/{id}/
PUT     /api/payments/{id}/
PATCH   /api/payments/{id}/
DELETE  /api/payments/{id}/
```

### Создание Stripe-платежа

Пример:

```http
POST /api/payments/
```

```json
{
    "paid_course": 1,
    "amount": "1500.00",
    "payment_method": "stripe"
}
```

После создания платежа API возвращает:

```json
{
    "id": 1,
    "payment_date": "2026-09-28T23:25:57.659296Z",
    "amount": "1500.00",
    "payment_method": "stripe",
    "payment_url": "https://checkout.stripe.com/...",
    "stripe_session_id": "cs_test_...",
    "user": 1,
    "paid_course": 1,
    "paid_lesson": null
}
```

`payment_url` можно открыть в браузере для перехода на тестовую страницу Stripe Checkout.

> Stripe в проекте используется в тестовом режиме. Реальная оплата не производится.

---

# Фильтрация и сортировка

Для платежей доступны фильтры:

```text
/api/payments/?paid_course=1
/api/payments/?paid_lesson=2
/api/payments/?payment_method=stripe
```

Фильтры можно комбинировать:

```text
/api/payments/?paid_course=1&payment_method=stripe
```

Сортировка:

```text
/api/payments/?ordering=payment_date
```

или:

```text
/api/payments/?ordering=-payment_date
```

---

# Пагинация

Курсы:

```text
/api/courses/?page=2
```

Уроки:

```text
/api/lessons/?page=2
```

Изменение размера страницы:

```text
/api/courses/?page_size=5
```

```text
/api/lessons/?page_size=10
```

Максимальный размер страницы — 10 объектов.

---

# Документация API

Для просмотра автоматически сгенерированной документации используются Swagger и ReDoc.

### Swagger

```text
http://127.0.0.1:8000/swagger/
```

### ReDoc

```text
http://127.0.0.1:8000/redoc/
```

Swagger позволяет просматривать доступные endpoints, параметры запросов и схемы ответов.

---

# Тестирование

Для запуска тестов:

```bash
poetry run python manage.py test
```

В проекте тестируются:

* CRUD операций;
* создание и изменение курсов;
* CRUD уроков;
* права владельцев;
* права модераторов;
* запрет доступа к чужим объектам;
* YouTube-валидация;
* подписки;
* повторная подписка;
* отписка;
* повторная отписка;
* поле `is_subscribed`;
* пагинация курсов;
* пагинация уроков.

## Coverage

Запуск покрытия:

```bash
poetry run coverage erase
poetry run coverage run manage.py test
poetry run coverage report
```

Для сохранения отчёта:

```bash
poetry run coverage report > coverage.txt
```

---

# Django Admin

Административная панель доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

Через неё можно управлять:

* пользователями;
* группами;
* курсами;
* уроками;
* подписками;
* платежами.

Для модераторов используется группа:

```text
Модераторы
```

---

# Stripe

Интеграция со Stripe вынесена в отдельный сервис:

```text
users/services/stripe_service.py
```

Сервис содержит функции для:

```text
create_stripe_product()
create_stripe_price()
create_checkout_session()
```

При создании платежа:

```text
Payment
   ↓
Stripe Product
   ↓
Stripe Price
   ↓
Stripe Checkout Session
   ↓
payment_url
```

Статус успешной оплаты на данный момент отдельно не проверяется, поскольку для текущей версии задания это не требуется.

---

# Безопасность

Секретные данные не должны храниться непосредственно в исходном коде.

В частности, не следует добавлять в Git:

```text
.env
```

и секретный ключ Stripe:

```text
sk_test_...
```

Для проекта рекомендуется использовать переменные окружения.

---

# Автор

**Sotocs**

GitHub:

https://github.com/Sotocs/DjangoREST
