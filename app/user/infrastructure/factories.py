from sqlalchemy.orm import Session
from app.user.infrastructure.repo.user import UserRepository
from app.user.domain.repo.user_repo_interface import IUserRepository
from app.user.infrastructure.repo.profile import ProfieRepository
from app.user.domain.repo.profile_repo_interface import IProfileRepository


class RepoFactory:
    def get_user_repo(self, db: Session) -> IUserRepository:
        return UserRepository(db)
    
    def get_profile_repo(self, db: Session) -> IProfileRepository:
        return ProfieRepository(db)