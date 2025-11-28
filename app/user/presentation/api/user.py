from fastapi import APIRouter, Depends

from uuid import UUID
from app.user.deps import get_user_service
from app.user.domain.models.user import User
from app.user.domain.services.user_service import UserService
from app.user.presentation.schemas.user import UserCreateSchema, UserOutSchema


router = APIRouter()


@router.post("/create")
def create_user(payload: UserCreateSchema, service: UserService = Depends(get_user_service)):
    service.create(username=payload.username)
    return {"message": "User created"}

@router.get("/{user_id}", response_model=UserOutSchema)
def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    user: User = service.get_by_id(user_id)
    
    return user