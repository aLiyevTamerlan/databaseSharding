from pydantic import BaseModel
from uuid import UUID
class UserBaseSchema(BaseModel):
    username: str

class ProfileBaseSchema(BaseModel):
    bio: str
    avatar_url : str

class UserCreateSchema(UserBaseSchema):
    profile: ProfileBaseSchema


class UserUpdateSchema(UserBaseSchema):
    pass

class UserOutSchema(UserBaseSchema):
    id: UUID
    model_config = {'from_attributes': True}