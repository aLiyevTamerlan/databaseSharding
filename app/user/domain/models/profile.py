from __future__ import annotations

import uuid

from typing import TYPE_CHECKING
from sqlalchemy import UUID, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from app.db.base import Base

if TYPE_CHECKING:

    from app.user.domain.models import User
class Profile(Base):
    __tablename__ = "profiles"
    

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
    bio = Column(String(500))
    avatar_url = Column(String(255))
    user: Mapped["User"] = relationship(back_populates="profile", uselist=False)