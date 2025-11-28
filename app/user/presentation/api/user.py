from fastapi import APIRouter, Depends

from app.user.deps import get_user_service
from app.user.domain.models.user import User
from app.user.domain.services.user_service import UserService
from app.user.presentation.schemas.user import UserCreateSchema


router = APIRouter()

@router.get("/")
def test(user_id: str):
    a = hash(user_id)
    print(-5122704023163466000 %3)
    return {"hash_value":a, "div_mod": -5122704023163466000 %3}


@router.post("/create")
def create_user(payload: UserCreateSchema, service: UserService = Depends(get_user_service)):
    service.create(username=payload.username)
    return {"message": "User created"}