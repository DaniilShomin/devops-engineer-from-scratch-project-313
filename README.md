### Hexlet tests and linter status:
[![Actions Status](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions)

### CI Status:
[![CI](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml/badge.svg)](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions)

## Описание

Сервис сокращения ссылок (URL shortener) на Flask с REST API для CRUD-операций над ссылками. Бэкенд использует SQLModel/SQLAlchemy и поддерживает SQLite (локально) и PostgreSQL (в продакшене). Для локальной разработки подключён готовый React-фронтенд через npm-пакет Hexlet.

## Запуск

Приложение использует [uv](https://docs.astral.sh/uv/) для управления зависимостями.

```bash
# Установка зависимостей
uv sync --all-groups

# Запуск бэкенда
make run
```

Приложение будет доступно по адресу http://localhost:8080.

Проверить работу можно с помощью curl:

```bash
curl http://localhost:8080/ping
```

Ожидаемый ответ: `pong`

### Локальная разработка с фронтендом

```bash
# Установка Node.js-зависимостей
npm install

# Одновременный запуск бэкенда и фронтенда
make dev
```

- Бэкенд: http://localhost:8080
- Фронтенд: http://localhost:5173

## Доступные команды

| Команда | Описание |
|---|---|
| `make run` | Запустить Flask-бэкенд на порту 8080 |
| `make dev` | Запустить фронтенд (5173) и бэкенд (8080) одновременно |
| `make test` | Запустить тесты (pytest) |
| `make lint` | Проверка линтера (ruff check + format check) |
| `make format` | Автоформатирование (ruff format) |

## API

| Метод | Путь | Описание |
|---|---|---|
| GET | `/ping` | Health-check, возвращает `pong` |
| GET | `/api/links` | Список ссылок (пагинация через `?range=[start,end]`) |
| POST | `/api/links` | Создать ссылку |
| GET | `/api/links/<id>` | Получить ссылку по ID |
| PUT | `/api/links/<id>` | Обновить ссылку |
| DELETE | `/api/links/<id>` | Удалить ссылку |

## Деплой

Приложение развёрнуто на Render:

**URL:** https://devops-engineer-from-scratch-project-313.onrender.com

### Локальный запуск через Docker

```bash
docker build -t devops-app .
docker run -p 8080:8080 -e PORT=8080 devops-app
```

### Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|---|---|---|
| `PORT` | Порт приложения | `8080` |
| `BASE_URL` | Базовый URL для коротких ссылок | `http://localhost:8080` |
| `DATABASE_URL` | URL базы данных | `sqlite:///app.db` |
| `SENTRY_DSN` | DSN для Sentry (опционально) | — |

## Линтинг и форматирование

- **ruff** — линтер и форматёр
- Конфигурация: `ruff.toml` (`target-version = "py313"`, `line-length = 88`)
- Перед коммитом выполняйте `make lint`
