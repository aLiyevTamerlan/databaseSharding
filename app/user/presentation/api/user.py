from fastapi import APIRouter

from app.user.domain.models.user import User
from app.user.presentation.schemas.user import UserCreateSchema


router = APIRouter()

@router.get("/")
def test(user_id: str):
    a = hash(user_id)
    print(-5122704023163466000 %3)
    return {"hash_value":a, "div_mod": -5122704023163466000 %3}


@router.post("/create")
def create_user(payload: UserCreateSchema):
    user = User(username=payload.username)
    print(user.id)
    return {"message": "User created"}