
from app.managers import SharedManager
from app.user.domain.services.user_service import UserService
from app.user.infrastructure.factories import user_repo_factory


def get_user_service() -> UserService:
    shared_manager = SharedManager()
    factory = user_repo_factory
    return UserService(shared_manager=shared_manager, repo_factory=factory)