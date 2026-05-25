### Hexlet tests and linter status:
[![Actions Status](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions)

### CI Status:
[![CI](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml/badge.svg)](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions)

## Запуск

Приложение использует [uv](https://docs.astral.sh/uv/) для управления зависимостями.

Для запуска выполните:

```bash
make run
```

Приложение будет доступно по адресу http://localhost:8080.

Проверить работу можно с помощью curl:

```bash
curl http://localhost:8080/ping
```

Ожидаемый ответ: `pong`

## Деплой

Приложение развёрнуто на Render:

**URL:** https://devops-engineer-from-scratch-project-313.onrender.com

### Локальный запуск через Docker

```bash
docker build -t devops-app .
docker run -p 8080:8080 -e PORT=8080 devops-app
```

### Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `PORT` | Порт, на котором запускается приложение | Нет (по умолчанию 8080) |
| `SENTRY_DSN` | DSN для мониторинга ошибок в Sentry | Нет |
| `DATABASE_URL` | URL базы данных | Нет |
| `BASE_URL` | Базовый URL для формирования коротких ссылок | Нет (по умолчанию `http://localhost:8080`)|
