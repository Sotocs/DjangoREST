# DjangoREST

REST API приложение на Django и Django REST Framework. Проект предоставляет API для работы с курсами, уроками, пользователями, подписками и платежами.

## Технологический стек

- Python 3.14
- Django 6
- Django REST Framework
- PostgreSQL 17
- Redis 7
- Celery
- Gunicorn
- Nginx
- Docker и Docker Compose
- WhiteNoise
- GitHub Actions

## Архитектура проекта

Приложение запускается в отдельных Docker-контейнерах:

| Сервис | Назначение |
|---|---|
| `web` | Django REST API, запускаемый через Gunicorn |
| `db` | База данных PostgreSQL |
| `redis` | Брокер сообщений и хранилище результатов Celery |
| `celery` | Выполнение фоновых задач |
| `celery-beat` | Планировщик периодических задач |
| `nginx` | Обратный прокси для обработки HTTP-запросов |

Nginx принимает внешние HTTP-запросы на порту 80 и перенаправляет их Django-приложению.

Статические файлы собираются при запуске контейнера и обслуживаются с помощью WhiteNoise.

PostgreSQL и Redis доступны другим сервисам через внутреннюю сеть Docker.

## Требования

Для запуска проекта с помощью Docker:

- Git
- Docker Engine
- Docker Compose v2

Для запуска без Docker дополнительно потребуются:

- Python 3.14
- Poetry
- PostgreSQL
- Redis

## Локальный запуск с Docker Compose

### 1. Клонирование репозитория

```bash
git clone https://github.com/Sotocs/DjangoREST.git
cd DjangoREST
```

### 2. Настройка переменных окружения

Создайте файл `.env` на основе примера:

```bash
cp .env.example .env
```

В Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Откройте `.env` и укажите необходимые значения, прежде всего `SECRET_KEY` и `DB_PASSWORD`.

Не публикуйте файл `.env` и не добавляйте его в Git.

### 3. Сборка и запуск контейнеров

```bash
docker compose up -d --build
```

Команда соберёт Docker-образ приложения и запустит все необходимые сервисы.

### 4. Применение миграций

```bash
docker compose exec web python manage.py migrate
```

### 5. Создание администратора

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Доступ к приложению

После запуска сервисов доступны:

- **Swagger:** http://localhost/swagger/
- **ReDoc:** http://localhost/redoc/
- **Django Admin:** http://localhost/admin/

## Полезные команды Docker Compose

Просмотр запущенных контейнеров:

```bash
docker compose ps
```

Просмотр логов Django:

```bash
docker compose logs -f web
```

Просмотр логов всех сервисов:

```bash
docker compose logs -f
```

Перезапуск сервисов:

```bash
docker compose restart
```

Остановка приложения:

```bash
docker compose down
```

Остановка приложения с удалением томов базы данных:

```bash
docker compose down -v
```

**Внимание:** последняя команда удаляет Docker-тома PostgreSQL и Redis, включая сохранённые данные базы данных.

## Тестирование и проверка качества кода

Установка зависимостей:

```bash
poetry install --with dev --no-root
```

Запуск тестов Django:

```bash
poetry run python manage.py test
```

Проверка конфигурации Django:

```bash
poetry run python manage.py check
```

Проверка сортировки импортов с помощью isort:

```bash
poetry run isort --check-only --profile black .
```

Проверка форматирования с помощью Black:

```bash
poetry run black --check .
```

## CI/CD и автоматический деплой

Конфигурация GitHub Actions находится в файле `.github/workflows/deploy.yml`.

Workflow запускается:

- при отправке изменений в ветки `main` и `develop`;
- при создании или обновлении Pull Request в `develop`;
- вручную через GitHub Actions.

### Этапы CI

1. Установка Python и Poetry.
2. Установка зависимостей проекта.
3. Проверка сортировки импортов с помощью isort.
4. Проверка форматирования кода с помощью Black.
5. Проверка конфигурации Docker Compose.
6. Сборка Docker-образа.
7. Проверка конфигурации Django.
8. Проверка отсутствия незапланированных миграций.
9. Запуск автоматических тестов.

### Автоматический деплой на VPS

После успешного прохождения CI отправка изменений в `main` запускает автоматический деплой на удалённый сервер.

Процесс деплоя:

1. Подключение к VPS по SSH.
2. Получение актуальной версии проекта из ветки `main`.
3. Проверка конфигурации Docker Compose.
4. Сборка обновлённого Docker-образа.
5. Запуск PostgreSQL и Redis.
6. Применение миграций базы данных.
7. Пересоздание контейнеров Django, Celery, Celery Beat и Nginx.

Для настройки подключения к VPS в GitHub Actions необходимо добавить следующие секреты репозитория:

| Секрет | Назначение |
|---|---|
| `VPS_HOST` | IP-адрес или домен сервера |
| `VPS_USER` | Пользователь SSH |
| `VPS_SSH_KEY` | Приватный SSH-ключ |
| `VPS_KNOWN_HOSTS` | Проверенный SSH host key |
| `VPS_APP_PATH` | Путь к проекту на сервере |

Секретные значения нельзя хранить непосредственно в репозитории.

## Репозиторий

GitHub: https://github.com/Sotocs/DjangoREST