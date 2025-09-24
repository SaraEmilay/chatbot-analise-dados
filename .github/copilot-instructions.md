## Repo overview

This repository is a small prototype FastAPI service that translates user chat messages into SQL and runs them against a Postgres dataset. Key pieces:

- `app/main.py` — FastAPI endpoints; the `/chat` POST is the primary integration point.
- `app/db.py` — Database connection and `run_sql(sql: str) -> pandas.DataFrame` helper. Uses SQLAlchemy `create_engine` and a hard-coded `DATABASE_URL`.
- `app/nl_to_sql_hf.py` — Transformer (T5) model loading and `generate_sql(user_question: str) -> str` that produces SQL from natural language.
- `app/endepoint.py` — example `requests` client showing how to call the running FastAPI server.
- `app/utils.py` — small helpers (e.g., `format_insight`) that convert query results into the response payload.
- `schema.md` — dataset schema (columns: REF_DATE, TARGET, VAR1..VAR6) which is critical when generating SQL or validating columns in queries.
- `train.gz` — the compressed dataset used in notebooks and local experimentation.

Keep these file paths in mind as the primary touchpoints when editing behavior, adding endpoints, or changing SQL generation.

## Big-picture architecture and dataflow

1. User sends a JSON {user_id, message} to `/chat`.
2. `main.chat` decides which SQL to run (currently simple string matching) or delegates to `nl_to_sql_hf.generate_sql` to synthesize SQL using a T5 model.
3. Generated SQL is executed via `app.db.run_sql` and returns a `pandas.DataFrame`.
4. `app.utils.format_insight` converts the DataFrame into the returned JSON payload.

Design notes discovered in code:
- The project is a prototype: many values are hard-coded (DB URL in `db.py`, simple rule in `main.py` to detect "média de idade por UF").
- The T5 model used is `mrm8488/t5-small-finetuned-wikiSQL` (see `nl_to_sql_hf.py`), so generated SQL will follow the model's output style and must be validated/sanitized before execution in production.

## Agent guidance: what to change and where

- To add a new chat behavior or SQL template, edit `app/main.py` (inside `chat`). Prefer adding small helper functions to `app/utils.py` for formatting or sanitization.
- When modifying DB behavior or connection parameters, update `app/db.py`. Move `DATABASE_URL` into environment variables (`os.environ`) for production deployments.
- To change or swap the NL→SQL model, edit `app/nl_to_sql_hf.py`. Keep the public helper `generate_sql(user_question: str) -> str` signature stable so callers in `main.py` don't need changes.

## Project-specific conventions and patterns

- Small, single-file modules that expose a focused function (e.g., `run_sql`, `generate_sql`) — maintain these public helper functions when refactoring.
- Prototype-first coding: expect hard-coded secrets and example clients (`app/endepoint.py`). When preparing changes for deployment, convert examples into tests or scripts under a `tests/` or `scripts/` folder.
- Data schema is authoritative in `schema.md`. Use those column names (REF_DATE, TARGET, VAR1..VAR6 / VAR5=UF, VAR6=classe social) when generating SQL or writing tests.

## Developer workflows (run, debug, test)

- Install dependencies listed in `requirements.txt`. Note: the current `requirements.txt` is empty in the repository; the notebook suggests `pandas`, `sqlalchemy`, `psycopg2-binary`, `jupyter`, and `transformers` are used. Typical install for local dev:

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
pip install pandas sqlalchemy psycopg2-binary jupyter transformers torch requests fastapi uvicorn
```

- Run the API locally:

```powershell
uvicorn app.main:app --reload --port 8000
```

- Example client call (from `app/endepoint.py`):

```powershell
python app/endepoint.py
```

- Notebook exploration: open `ingest.ipynb` — it demonstrates loading `train.gz` with `pandas` and shows quick EDA commands.

## Integration points & external dependencies

- Postgres: `app/db.py` expects a Postgres database at `postgresql://postgres:senha@localhost:5432/meu_banco`. Agents modifying DB behavior should either use env vars or reference `DATABASE_URL` directly when running locally.
- Hugging Face Transformers: `nl_to_sql_hf.py` downloads `mrm8488/t5-small-finetuned-wikiSQL`. Large model downloads and GPU/CPU constraints apply.
- `train.gz` dataset used for local tests and notebook experiments.

## Safety and validation notes for AI agents

- Never execute arbitrary generated SQL without validation. The codebase currently executes model output directly via `run_sql` — when adding or updating, add a sanitization step in `app/utils.py` or a dedicated `validate_sql(sql: str) -> bool` function.
- Prefer returning safe, truncated results (the existing `format_insight` returns first 10 rows) instead of full table dumps.

## Quick examples (copyable)

- Run server: `uvicorn app.main:app --reload --port 8000`
- Call `/chat` using the example `app/endepoint.py` or with `curl`/`requests` as shown in that file.
- Change DB URL: update `DATABASE_URL` in `app/db.py` to use an environment variable: `os.getenv('DATABASE_URL', 'postgresql://...')`.

## Files to inspect for future changes

- `app/main.py` — API logic and primary entrypoint
- `app/db.py` — DB connection
- `app/nl_to_sql_hf.py` — model & tokenization
- `app/utils.py` — formatting and small helpers
- `schema.md` — dataset schema (authoritative for column names)

---

If you'd like, I can (a) add a small `validate_sql` helper and wire it before `run_sql`, (b) populate `requirements.txt` with explicit versions, or (c) add a `README.md` with quick run instructions. Which should I do next? 
