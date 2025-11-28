import uuid
from sqlalchemy import UUID, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Profile(Base):
    __tablename__ = "profiles"
    
    # Local unique ID - can use database default
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # OK to use default here
        unique=True,
        nullable=False,
    )
    # SHARDING KEY - this determines which shard!
    user_id = Column(Integer, nullable=False, index=True)
    bio = Column(String(500))
    avatar_url = Column(String(255))