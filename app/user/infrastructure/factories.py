from sqlalchemy.orm import Session
from app.user.infrastructure.repo.user import UserRepository
from app.user.domain.repo.user_repo_interface import IUserRepository



class RepoFactory:
    def get_user_repo(self, db: Session) -> IUserRepository:
        return UserRepository(db)