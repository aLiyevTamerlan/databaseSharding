from sqlalchemy.orm import Session
from app.user.infrastructure.repo.user import UserRepository
from app.user.domain.repo.user_repo_interface import IUserRepository

def user_repo_factory(db: Session) -> IUserRepository:

    return UserRepository(db)