# db/shards.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URLS = {
    0: "sqlite:///./shard_0.db",
    1: "sqlite:///./shard_1.db",
}

engines = {
    shard_id: create_engine(url, echo=True)
    for shard_id, url in DATABASE_URLS.items()
}

session_makers = {
    shard_id: sessionmaker(bind=engine)
    for shard_id, engine in engines.items()
}
