from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.user.domain.models import Profile
from app.user.domain.repo.profile_repo_interface import IProfileRepository


class ProfieRepository(IProfileRepository):
    def __init__(self, db: Session):
        self._db = db

    def create(self, profile: Profile) -> Profile:
        self._db.add(profile)
        self._db.commit()
        self._db.refresh(profile)
        return profile