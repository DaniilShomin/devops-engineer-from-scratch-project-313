### Hexlet tests and linter status:
[![Actions Status](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DaniilShomin/devops-engineer-from-scratch-project-313/actions)

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
