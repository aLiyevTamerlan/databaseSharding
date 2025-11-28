from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.user.domain.models.user import User
from app.user.domain.repo.user_repo_interface import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self._db = db

    def get_all(self) -> List[User]:
        return self._db.query(User).all()

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return (
            self._db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create(self, user: User) -> User:
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update(self, db_user: User, data: dict) -> User:
        for key, value in data.items():
            setattr(db_user, key, value)

        self._db.commit()
        self._db.refresh(db_user)
        return db_user

    def delete(self, user_id: UUID) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        self._db.delete(user)
        self._db.commit()
        return True
