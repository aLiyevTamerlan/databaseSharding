
from app.managers import SharedManager
from app.user.domain.services.user_service import UserService
from app.user.infrastructure.factories import user_repo_factory


def get_shared_manager() -> SharedManager:
    return SharedManager()

def get_user_service() -> UserService:
    factory = user_repo_factory
    return UserService(repo_factory=factory)