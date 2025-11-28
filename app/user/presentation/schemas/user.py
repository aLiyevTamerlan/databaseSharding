from pydantic import BaseModel
from uuid import UUID
class UserBaseSchema(BaseModel):
    username: str

class UserCreateSchema(UserBaseSchema):
    pass

class UserUpdateSchema(UserBaseSchema):
    pass

class UserOutSchema(UserBaseSchema):
    id: UUID
    model_config = {'from_attributes': True}