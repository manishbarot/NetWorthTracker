# AGENTS.md

## Orientation

This repo holds two stacks; only one is real.

- **Active app: Flask POC at the repo root** (`poc_app.py`, `models.py`, `templates/`, `static/`). This is where all recent work happens (see git history). Runs on port **5001**.
- **Scaffold: Node workspaces** (`frontend/`, `backend/`, root `package.json`). The README describes this as the main stack, but `backend/src` and `frontend/src` contain only placeholder entrypoints (`server.ts`, `main.tsx`) and there are **no tests**. Treat README claims about the Node stack as aspirational, not current reality.

## Flask POC

Run:

```powershell
poc_venv\Scripts\Activate   # or `venv\Scripts\Activate`
python poc_app.py           # -> http://127.0.0.1:5001
```

Dependencies: `pip install -r poc_requirements.txt` (not `requirements.txt`, which targets the future full app).

**DB setup gotcha:** `poc_app.py` never creates tables (its `__main__` block runs `app.run()` only). On a fresh checkout, run in order:

```powershell
python create_db.py   # creates tables in instance/poc_networth.db
python init_db.py     # seeds AccountType / AssetType / LiabilityType rows
```

`poc_networth.db` lives in `instance/` and is gitignored.

`app.py` is a separate, fuller Flask app (port 5000, `DATABASE_URL` from `.env`). Both share `models.py`, but they wire SQLAlchemy differently — note the mismatch:
- `poc_app.py`: `db.init_app(app)` — correct.
- `app.py`: creates a **new** `db = SQLAlchemy(app)` while models register themselves on `models.db` (unbound). `app.py` is therefore inconsistent with the models and may not create/query tables properly.

Don't "fix" `app.py`'s wiring while changing models unless asked; `poc_app.py` is the source of truth.

## Python root scripts

`check_*.py`, `create_*.py`, `migrate_*.py`, `test_*.py`, `reset_*.py`, etc. at the root are **ad-hoc one-off scripts**, not a test suite or tooling. There is no pytest config, no Python lint config (black/flake8 are listed in `requirements.txt` but unconfigured), and no CI. Recreating/renaming these is safe; don't add them to any build.

## Node workspaces

- npm workspaces: `frontend/`, `backend/`. Note root scripts use `cd <pkg> && ...` rather than `npm -w`.
- `npm run dev` (both), `npm run dev:backend` / `npm run dev:frontend`, `npm test`, `npm run lint`, `npm run type-check` run per package via `cd`.
- `npm run db:up` starts Postgres/TimescaleDB + Redis via `docker-compose.yml` (required before `npm run dev`).

## Environment

- Flask reads `.env` via `python-decouple`; POC uses `SECRET_KEY` and `ALPHA_VANTAGE_API_KEY` (both default to harmless values, so the app runs without `.env`).
- Root `.env.example` targets the Node/Postgres stack, not the POC.