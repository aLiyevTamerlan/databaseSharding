# db/shards.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URLS = {
    0: "postgresql://postgres:postgres@localhost:5432/shard_0",
    1: "postgresql://postgres:postgres@localhost:5432/shard_1",
}


engines = {
    shard_id: create_engine(url, echo=False)
    for shard_id, url in DATABASE_URLS.items()
}

session_makers = {
    shard_id: sessionmaker(bind=engine)
    for shard_id, engine in engines.items()
}
