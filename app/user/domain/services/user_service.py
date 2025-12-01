from typing import Optional, Callable, Sequence
from uuid import  UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.user.domain.models.user import User
from app.user.domain.repo.user_repo_interface import IUserRepository
from app.user.infrastructure.factories import RepoFactory
from app.user.infrastructure.repo.profile import ProfieRepository
from app.user.ports.user_protorocls import IProfileReader
from app.user.presentation.schemas.user import UserCreateSchema, UserOutSchema

class UserService:
    def __init__(self, 
                 repo_factory: RepoFactory) -> None:
        self._repo_factory = repo_factory
        
    def get_all(self, db: Session) -> Sequence[User]:
        repo = self._repo_factory.get_user_repo(db)
        return repo.get_all()

    def get_by_id(self, user_id: UUID, db: Session) -> UserOutSchema:
        
        repo = self._repo_factory.get_user_repo(db)
        user = repo.get_by_id(user_id)
        

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserOutSchema.model_validate(user)

    def create(self, data: UserCreateSchema, user_id: UUID, db: Session) -> User:
        new_user = User(
            id=user_id,
            **data.model_dump(),
        )
        repo = self._repo_factory.get_user_repo(db)
        return repo.create(new_user)

    def update(self, user_id: UUID, data: dict, db: Session) -> Optional[User]:
        repo = self._repo_factory.get_user_repo(db)
        user = repo.get_by_id(user_id)
        updated_user = repo.update(user, data)
        return UserOutSchema.model_validate(updated_user)
    
    
    def delete(self, user_id: UUID, db: Session) -> bool:
        repo = self._repo_factory.get_user_repo(db)
        user = repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return repo.delete(user_id=user_id)

