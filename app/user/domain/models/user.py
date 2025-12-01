from __future__ import annotations


import uuid
from typing import TYPE_CHECKING
from sqlalchemy import UUID, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from app.db.base import Base

if TYPE_CHECKING:
    from app.user.domain.models.profile import Profile
    

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    username = Column(String, nullable=False)

    profile: Mapped["Profile"] = relationship(
        "Profile",  # Use string reference
        back_populates="user",
        uselist=False,
        # lazy='select'
    )