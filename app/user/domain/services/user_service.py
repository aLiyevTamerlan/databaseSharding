from typing import List, Optional, Callable
from uuid import uuid4, UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.user.domain.models.user import User
from app.user.domain.repo.user_repo_interface import IUserRepository
from app.managers import SharedManager
from app.user.presentation.schemas.user import UserOutSchema

class UserService:
    def __init__(self, repo_factory: Callable[[Session], IUserRepository]) -> None:
        self._repo_factory = repo_factory
        
    def get_all(self, db: Session) -> List[User]:
        pass

    def get_by_id(self, user_id: UUID, db: Session) -> UserOutSchema:
        
        repo = self._repo_factory(db)
        user = repo.get_by_id(user_id)
        

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserOutSchema.model_validate(user)

    def create(self, username: str, db: Session) -> User:
        user_id = uuid4()
        new_user = User(
            id=user_id,
            username=username,
        )
        with self._shared_manager.get_session(entity_id=user_id) as db:
            repo = self._repo_factory(db)
        return repo.create(new_user)

    def update(self, user_id: UUID, data: dict, db: Session) -> Optional[User]:
        repo = self._repo_factory(db)
        user = repo.get_by_id(user_id)
        updated_user = repo.update(user, data)
        return UserOutSchema.model_validate(updated_user)
    
    
    def delete(self, user_id: UUID, db: Session) -> bool:
        repo = self._repo_factory(db)
        user = repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return repo.delete(user_id=user_id)

