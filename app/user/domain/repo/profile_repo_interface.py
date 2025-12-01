from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.user.domain.models import Profile


class IProfileRepository(ABC):
    @abstractmethod
    def create(self, profile: Profile) -> Profile:
        pass
