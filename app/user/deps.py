
from app.managers import SharedManager
from app.user.domain.services.user_service import UserService
from app.user.infrastructure.factories import RepoFactory


def get_shared_manager() -> SharedManager:
    return SharedManager()

def get_user_service() -> UserService:
    factory = RepoFactory()
    return UserService(repo_factory=factory)