# Подключение фронтенда и CORS для URL shortener

## Дата
2025-05-25

## Контекст
Проект URL shortener на Flask с API (`/api/links`, `/ping`, `/sentry-debug`) и SQLModel/PostgreSQL. Необходимо подключить готовый фронтенд-пакет, настроить CORS для локальной разработки и обеспечить одновременный запуск фронтенда и бэкенда.

## Цель
1. Установить `@hexlet/project-devops-deploy-crud-frontend` и запустить его локально
2. Настроить CORS на бэкенде для запросов с `http://localhost:5173`
3. Обеспечить одновременный запуск фронтенда и бэкенда через `concurrently`
4. Фронтенд должен корректно взаимодействовать с API

## Архитектура

### Зависимости
- **Python**: добавить `flask-cors` в `pyproject.toml` (runtime-зависимость)
- **Node.js**: создать `package.json` в корне проекта с dev-зависимостями:
  - `@hexlet/project-devops-deploy-crud-frontend`
  - `concurrently`

### Запуск (локальная разработка)
- Скрипт в `package.json`:
  ```json
  "dev": "concurrently \"npx start-hexlet-devops-deploy-crud-frontend\" \"uv run python main.py\""
  ```
- Команда `make dev` в `Makefile`, которая вызывает `npm run dev`
- Фронтенд слушает на `localhost:5173` (фиксированный порт пакета)
- Бэкенд слушает на `localhost:8080`

### CORS
- В `main.py` инициализировать `flask_cors.CORS`:
  - `origins`: `["http://localhost:5173"]`
  - `methods`: `["GET", "POST", "PUT", "DELETE", "OPTIONS"]`
  - `allow_headers`: `["Content-Type", "Content-Range"]`
  - `expose_headers`: `["Content-Range"]`
- CORS middleware применяется глобально ко всем маршрутам

### Продакшен (Render)
- Фронтенд раздаётся Caddy (следующий шаг), запуск через `concurrently` нужен только для локальной разработки
- Dockerfile не изменяется — Node.js зависимости не нужны в продакшен-образе
- Убедиться, что `node_modules` и `package.json` не попадают в Docker-образ (`.dockerignore`)

## Тестирование
- Запустить `make dev`
- Открыть `http://localhost:5173`
- Убедиться, что:
  - Загружается UI
  - Создание, просмотр, редактирование, удаление ссылок работает
  - Пагинация работает и отображается корректно

## Миграции/Изменения файлов
- `pyproject.toml`: добавить `flask-cors>=4.0`
- `main.py`: добавить импорт `flask_cors` и инициализацию CORS
- `Makefile`: добавить цель `dev`
- Создать: `package.json`, `.dockerignore` (если отсутствует)

## Критерии приёмки
- [ ] `node -v` возвращает версию >= 20
- [ ] `npm install @hexlet/project-devops-deploy-crud-frontend` выполняется без ошибок
- [ ] `make dev` запускает одновременно фронтенд и бэкенд
- [ ] Фронтенд доступен по `http://localhost:5173`
- [ ] API-запросы с фронтенда проходят без CORS-ошибок
- [ ] Все CRUD-операции и пагинация работают через UI
- [ ] Тесты бэкенда продолжают проходить (`make test`)
