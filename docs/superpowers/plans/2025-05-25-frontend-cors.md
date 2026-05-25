# Frontend + CORS Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Подключить готовый фронтенд-пакет, настроить CORS для локальной разработки и обеспечить одновременный запуск фронтенда и бэкенда.

**Architecture:** В корне проекта создаём `package.json` с фронтенд-пакетом и `concurrently`. Добавляем `flask-cors` в Python-зависимости. В `main.py` инициализируем CORS middleware. В `Makefile` добавляем команду `dev`, запускающую оба процесса параллельно.

**Tech Stack:** Flask, flask-cors, SQLModel, Node.js, npm, concurrently

---

### Task 1: Add flask-cors to Python dependencies

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add flask-cors to dependencies**

```toml
[project]
dependencies = [
    "flask>=3.1.3",
    "flask-cors>=4.0",
    "psycopg2-binary>=2.9.12",
    "python-dotenv>=1.2.2",
    "sentry-sdk[flask]>=2.0",
    "sqlmodel>=0.0.38",
]
```

- [ ] **Step 2: Sync Python dependencies**

```bash
uv sync --no-dev
```

Expected: dependencies synced, `flask-cors` available in `.venv`

- [ ] **Step 3: Verify flask-cors is importable**

```bash
uv run python -c "from flask_cors import CORS; print('OK')"
```

Expected output: `OK`

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "deps: add flask-cors"
```

---

### Task 2: Add CORS middleware to Flask app

**Files:**
- Modify: `main.py`
- Test: `tests/test_main.py`

- [ ] **Step 1: Write failing CORS test**

Add to `tests/test_main.py`:

```python
def test_cors_headers_on_api(client):
    response = client.options(
        "/api/links",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("Access-Control-Allow-Origin") == "http://localhost:5173"
    assert "GET" in response.headers.get("Access-Control-Allow-Methods", "")


def test_cors_headers_on_regular_request(client):
    response = client.get(
        "/api/links",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert response.headers.get("Access-Control-Allow-Origin") == "http://localhost:5173"
    assert response.headers.get("Access-Control-Expose-Headers", "") == "Content-Range"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_main.py::test_cors_headers_on_api -v
```

Expected: FAIL — `Access-Control-Allow-Origin` header missing (likely 404 for OPTIONS if not handled, or empty headers)

- [ ] **Step 3: Add CORS to main.py**

Modify `main.py` — add import and initialize CORS after app creation:

```python
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    origins=["http://localhost:5173"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Content-Range"],
    expose_headers=["Content-Range"],
)
```

Insert `from flask_cors import CORS` after line 6 (after `from flask import Flask, jsonify, request`) and insert the `CORS(...)` call after line 16 (after `app = Flask(__name__)`).

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_main.py -v
```

Expected: all tests pass including new CORS tests

- [ ] **Step 5: Commit**

```bash
git add main.py tests/test_main.py
git commit -m "feat: add CORS middleware for frontend integration"
```

---

### Task 3: Create package.json and install Node.js dependencies

**Files:**
- Create: `package.json`

- [ ] **Step 1: Create package.json**

```json
{
  "name": "devops-engineer-from-scratch-project-313",
  "private": true,
  "devDependencies": {
    "@hexlet/project-devops-deploy-crud-frontend": "latest",
    "concurrently": "^8.2.2"
  },
  "scripts": {
    "dev": "concurrently \"npx start-hexlet-devops-deploy-crud-frontend\" \"uv run python main.py\""
  }
}
```

- [ ] **Step 2: Install npm packages**

```bash
npm install
```

Expected: `node_modules/` created, `@hexlet/project-devops-deploy-crud-frontend` and `concurrently` installed.

- [ ] **Step 3: Verify frontend package is installed**

```bash
ls node_modules/@hexlet/project-devops-deploy-crud-frontend
```

Expected: directory exists with package contents

- [ ] **Step 4: Commit**

```bash
git add package.json package-lock.json
git commit -m "deps: add frontend package and concurrently"
```

---

### Task 4: Add Makefile target for concurrent dev run

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Add `dev` target to Makefile**

```makefile
dev:
	npm run dev
```

Append after existing `format:` target.

- [ ] **Step 2: Verify `make dev` starts both processes**

```bash
timeout 10 make dev || true
```

Expected: output shows both "start-hexlet-devops-deploy-crud-frontend" and "uv run python main.py" starting up.

- [ ] **Step 3: Commit**

```bash
git add Makefile
git commit -m "build: add 'make dev' to run frontend and backend concurrently"
```

---

### Task 5: Exclude Node.js files from Docker image

**Files:**
- Create: `.dockerignore`

- [ ] **Step 1: Create .dockerignore**

```
node_modules
package.json
package-lock.json
```

- [ ] **Step 2: Verify Docker build still works**

```bash
docker build -t devops-app-test .
```

Expected: build succeeds without including node_modules

- [ ] **Step 3: Commit**

```bash
git add .dockerignore
git commit -m "chore: add .dockerignore to exclude node_modules from Docker image"
```

---

## Self-Review

**Spec coverage:**
- ✅ Установка Node.js — проверяется пользователем (Task 3)
- ✅ Установка `@hexlet/project-devops-deploy-crud-frontend` — Task 3
- ✅ CORS middleware с нужными origins, methods, headers — Task 2
- ✅ `concurrently` для общего запуска — Task 3, Task 4
- ✅ Фронтенд на `localhost:5173`, бэкенд на `localhost:8080` — Task 4

**Placeholder scan:**
- ✅ Нет TBD/TODO
- ✅ Нет "appropriate error handling"
- ✅ Все шаги содержат конкретный код и команды
- ✅ Нет "similar to Task N"

**Type consistency:**
- ✅ Все импорты (`flask_cors.CORS`, `concurrently`) используются корректно
- ✅ Параметры CORS соответствуют заданию

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2025-05-25-frontend-cors.md`.

Two execution options:

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
