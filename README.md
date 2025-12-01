# Database Hash Sharding on FastAPI

A FastAPI demo showing how to spread data across PostgreSQL shards using a simple hash strategy. Each request is routed to a shard-specific SQLAlchemy session, with Alembic configured to migrate every shard.

## Architecture
- `main.py` boots FastAPI and mounts user routes under `/auth`.
- `app/db/session.py` lists shard connection strings (`DATABASE_URLS`) and builds per-shard engines/sessionmakers.
- `app/managers.py` provides `SharedManager`, which hashes an entity id (`hash(id) % shard_count`) to pick the shard and exposes `get_session`/`get_all_sessions` context managers.
- `app/user/domain` holds entities (`User`, `Profile`) and service logic (`UserService`) with repository interfaces.
- `app/user/infrastructure` implements the repositories for SQLAlchemy and a `RepoFactory` that wires them.
- `app/user/presentation` exposes FastAPI routes and Pydantic schemas.
- `alembic/env.py` iterates over all shard engines so `alembic upgrade head` applies to each shard.

## Project layout
- `app/db/base.py` – SQLAlchemy declarative base
- `app/db/session.py` – shard map and session factories
- `app/managers.py` – shard selection + session management helpers
- `app/user/presentation/api/user.py` – REST endpoints
- `app/user/domain/services/user_service.py` – user CRUD + profile handling
- `app/user/infrastructure/repo/` – SQLAlchemy repository implementations
- `alembic/` – migration config; `alembic/versions/*` holds schema revisions

## Sharding behavior
- Writes: `SharedManager.get_session(entity_id=user_id)` hashes the UUID and opens the matching shard session so a user and its profile land on the same shard.
- Reads by id: use the same hash to target the correct shard.
- List all: `get_all_sessions()` opens sessions for every shard and aggregates results.

## Running locally
1) **PostgreSQL shards:** Create databases (e.g., `shard_0`, `shard_1`) and ensure credentials match `app/db/session.py` (`postgres:postgres` by default). Update the `DATABASE_URLS` map if needed.
2) **Install deps:** `python -m venv .venv && .\\.venv\\Scripts\\activate` then `pip install .` (uses `pyproject.toml`).
3) **Migrate all shards:** `alembic upgrade head` (runs against every URL in `DATABASE_URLS`).
4) **Run the API:** `uvicorn main:app --reload` and hit `http://127.0.0.1:8000/docs` for Swagger.

### Example requests
- Create user
```json
POST /auth/
{
  "username": "jane",
  "profile": {"bio": "Loves shards", "avatar_url": "https://example.com/a.png"}
}
```
- Fetch with profile: `GET /auth/{user_id}`
- Update username: `PUT /auth/{user_id}` with `{ "username": "newname" }`
- Delete: `DELETE /auth/{user_id}`

## Extending
- Add shards by appending to `DATABASE_URLS`; `SharedManager` picks them up automatically.
- Add new domains by following the same presentation ? service ? repository ? model structure and adding Alembic migrations for their tables.
