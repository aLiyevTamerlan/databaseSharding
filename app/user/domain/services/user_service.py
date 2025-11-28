from typing import List, Optional, Callable
from uuid import uuid4, UUID

from sqlalchemy.orm import Session
from app.user.domain.models.user import User
from app.user.domain.repo.user_repo_interface import IUserRepository
from app.managers import SharedManager

class UserService:
    def __init__(self, shared_manager: SharedManager, repo_factory: Callable[[Session], IUserRepository]) -> None:
        self._shared_manager = shared_manager
        self._repo_factory = repo_factory
        
    def get_all(self) -> List[User]:
        pass

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        with self._shared_manager.get_session(entity_id=user_id) as db:
            repo = self._repo_factory(db)
        return repo.get_by_id(user_id)

    def create(self, username: str) -> User:
        user_id = uuid4()
        new_user = User(
            id=user_id,
            username=username,
        )
        with self._shared_manager.get_session(entity_id=user_id) as db:
            repo = self._repo_factory(db)
        return repo.create(new_user)

    def update(self, user_id: UUID, data: dict) -> Optional[User]:
        pass

    def delete(self, user_id: UUID) -> bool:
        pass
