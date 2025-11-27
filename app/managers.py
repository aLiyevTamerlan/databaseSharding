from contextlib import contextmanager

from app.db.session import DATABASE_URLS



class SharedManager:
    def __init__(self, shared_nums: int) -> None:
        self.shared_nums = shared_nums

    def get_shard_id(self, entity_id: int) -> int:
        return hash(entity_id) % self.shared_nums
    
    def get_session_maker(self, entity_id: int, shard_sessions: dict[int, any]) -> any:
        shard_id = self.get_shard_id(entity_id)
        return shard_sessions[shard_id]
    
    @contextmanager
    def get_session(self, entity_id: int):

        session_maker = self.get_session_maker(entity_id)
        session = session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

shared_manager = SharedManager(shared_nums=len(DATABASE_URLS))