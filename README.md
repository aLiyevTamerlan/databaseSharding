# Database Hash Sharding on FastAPI

A FastAPI demo showing how to spread data across PostgreSQL shards using a simple hash strategy. Each request is routed to a shard-specific SQLAlchemy session, with Alembic configured to migrate every shard.

## Why hash sharding and how it works
- Goal: split a growing dataset across multiple databases ("shards") to spread load and storage.
- Hash function: compute `shard_id = hash(entity_key) % shard_count`; stateless routing with no lookup tables.
- Even distribution: good hashes + UUID/int keys yield uniform spread, reducing hot spots.
- Locality: pick a sharding key that keeps related rows together (user + profile) to avoid cross-shard joins.
- Isolation: each shard is an independent DB; one shard failing is less likely to take down others.
- Scaling: add shards by expanding the hash space (or use consistent hashing to limit data movement).
- Trade-offs: global queries need fan-out/aggregation; cross-shard transactions are hard; reshuffling when shard count changes can be expensive; secondary-key lookups may need scatter/gather or denormalized indexes.

### Consistent hashing vs modulo
- Modulo (`hash % N`) is simple but changing `N` forces many keys to move.
- Consistent hashing moves only a fraction of keys when adding/removing shards and is better if you expect frequent resharding.

## Architecture
- `main.py` boots FastAPI and mounts user routes under `/auth`.
- `app/db/config.py` loads shard URLs from `.env` (`DB_SHARDS`).
- `app/db/session.py` maps shard IDs to URLs and builds per-shard engines/sessionmakers.
- `app/managers.py` provides `SharedManager`, which hashes an entity id to pick the shard and exposes `get_session`/`get_all_sessions` context managers.
- `app/user/domain` holds entities (`User`, `Profile`) and service logic (`UserService`) with repository interfaces.
- `app/user/infrastructure` implements the repositories for SQLAlchemy and a `RepoFactory` that wires them.
- `app/user/presentation` exposes FastAPI routes and Pydantic schemas.
- `alembic/env.py` iterates over all shard engines so `alembic upgrade head` applies to each shard.

## Project layout
- `app/db/base.py` - SQLAlchemy declarative base
- `app/db/config.py` - Pydantic settings loader for shard URLs
- `app/db/session.py` - shard map and session factories
- `app/managers.py` - shard selection + session management helpers
- `app/user/presentation/api/user.py` - REST endpoints
- `app/user/domain/services/user_service.py` - user CRUD + profile handling
- `app/user/infrastructure/repo/` - SQLAlchemy repository implementations
- `alembic/` - migration config; `alembic/versions/*` holds schema revisions

## Sharding behavior
- Writes: `SharedManager.get_session(entity_id=user_id)` hashes the UUID and opens the matching shard session so a user and its profile land on the same shard.
- Reads by id: use the same hash to target the correct shard.
- List all: `get_all_sessions()` opens sessions for every shard and aggregates results.

## Environment (.env)
Create a `.env` file in the project root:
```
DB_SHARDS="postgresql://USER:PASS@HOST:PORT/shard_0,postgresql://USER:PASS@HOST:PORT/shard_1"
```
- Comma-separated DSNs; order defines shard IDs (index 0, 1, 2, ...).
- Add more shards by appending more URLs.

## Running locally
1) **PostgreSQL shards:** Create databases (e.g., `shard_0`, `shard_1`) and set `DB_SHARDS` accordingly in `.env`.
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
- Add shards by appending to `DB_SHARDS`; `SharedManager` picks them up automatically.
- Add new domains by following the same presentation -> service -> repository -> model structure and adding Alembic migrations for their tables.
