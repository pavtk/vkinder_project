# VKinder

Бот для знакомств ВКонтакте. Ищет кандидатов по возрасту, полу и городу, показывает топ-3 фото профиля, позволяет сохранять понравившихся в избранное.

## Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vkinder
DB_USER=postgres
DB_PASS=postgres
```

---

## Развёртывание базы данных

### Способ 1 — Docker (рекомендуется)

Требования: установленный [Docker](https://docs.docker.com/get-docker/).

```bash
docker compose up -d
```

База данных будет доступна на `localhost:5432`. Таблицы создадутся автоматически при первом запуске бота.

Остановить базу:

```bash
docker compose down
```

Остановить и удалить данные:

```bash
docker compose down -v
```

---

### Способ 2 — Локальный PostgreSQL

Требования: установленный PostgreSQL.

1. Подключитесь к PostgreSQL:

```bash
psql -U postgres
```

2. Создайте базу данных и пользователя:

```sql
CREATE DATABASE vkinder;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE vkinder TO postgres;
```

3. Укажите параметры подключения в `.env` (см. выше).

Таблицы создадутся автоматически при первом запуске бота.

---

## Запуск

```bash
pip install -r requirements.txt
python main.py
```
