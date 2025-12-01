from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.user.domain.models import User


class IUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User, data: dict) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass
