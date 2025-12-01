# db/shards.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.config import settings

DATABASE_URLS = {
   shard_id:settings.get_shards[shard_id]  for shard_id in range(len(settings.get_shards))
}

engines = {
    shard_id: create_engine(url, echo=False)
    for shard_id, url in DATABASE_URLS.items()
}

session_makers = {
    shard_id: sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        # expire_on_commit=False,
    )
    for shard_id, engine in engines.items()
}
