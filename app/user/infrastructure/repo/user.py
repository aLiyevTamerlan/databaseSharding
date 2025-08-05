from typing import List, Optional
from sqlalchemy.orm import Session

from app.user.domain.models.user import User
from app.user.domain.repo.user_repo_interface import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[User]:
        return self.db.query(User)

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, User: User) -> User:
        self.db.add(User)
        self.db.commit()
        self.db.refresh(User)
        return User

    def update(
            self,
            db_user: User,
            data: dict
    ) -> User:
        for key, value in data.Users():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
