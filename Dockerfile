FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости (без dev)
RUN uv sync --frozen --no-dev

# Копируем код приложения
COPY . .

# Порт, который будет слушать приложение
EXPOSE 8080

# Запуск приложения
CMD ["uv", "run", "--no-dev", "python", "main.py"]
