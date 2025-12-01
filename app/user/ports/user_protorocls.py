
from profile import Profile
from typing import Protocol


class IProfileReader(Protocol):
    def create(self, profile: Profile) -> Profile: ...