# Agent Notes

## Toolchain
- Python 3.13 is required. Use `uv` for all Python operations — never `pip`.
- The frontend is a pre-built Hexlet package (`@hexlet/project-devops-deploy-crud-frontend`), not source code in this repo.

## Common Commands
| Command | What it does |
|---|---|
| `make run` | Start the Flask backend on port 8080 |
| `make test` | Run pytest (`uv run pytest`) |
| `make lint` | Run ruff check + format check |
| `make format` | Auto-format with ruff |
| `make dev` | Start frontend (port 5173) and backend (port 8080) concurrently |

## Testing
- Tests live in `tests/test_main.py`.
- The `client` pytest fixture sets `TESTING=True` and uses an in-memory SQLite database.
- Run a single test: `uv run pytest tests/test_main.py -k <test_name>`

## Lint / Format
- Config: `ruff.toml` (`target-version = "py313"`, `line-length = 88`).
- Always run `make lint` before committing; CI enforces it.

## Database
- Default: SQLite (`sqlite:///app.db`).
- PostgreSQL: set `DATABASE_URL` env var.
- `database.py` defines the `Link` model and `init_db`/`get_session` helpers.

## Environment
- `.env` is gitignored but may be present locally. It contains `SENTRY_DSN`.
- `load_dotenv()` is called in `main.py`.
- Other env vars: `PORT` (default 8080), `BASE_URL` (default `http://localhost:8080`).

## Frontend Integration
- `npm run dev` starts the Hexlet React Admin frontend on `http://localhost:5173`.
- Backend CORS is hardcoded to `http://localhost:5173` in `main.py`.
- To change the allowed origin, edit the `CORS(...)` call in `main.py`.

## CI
- `.github/workflows/ci.yml` runs on push/PR to `main`.
- Steps: `uv sync --all-groups` → `uv run ruff check .` → `uv run pytest`.
- Do not edit `.github/workflows/hexlet-check.yml` — it is required by Hexlet.

## Docker
- `docker build -t devops-app .` then `docker run -p 8080:8080 -e PORT=8080 devops-app`.
- Uses `ghcr.io/astral-sh/uv:python3.13-bookworm-slim` base image.

## Secrets / Leak Prevention
- `.env` must never be committed. It is gitignored; verify with `git status` before committing.
- `app.db` (local SQLite) is also gitignored.
- No secrets, tokens, or passwords should be hardcoded in `main.py`, `database.py`, CI configs, or Dockerfiles.
- If rotating Sentry DSN, generate a new key in the Sentry dashboard and update `.env` locally.
