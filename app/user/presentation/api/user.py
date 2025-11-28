from fastapi import APIRouter, Depends

from uuid import UUID, uuid4
from app.user.deps import get_user_service, get_shared_manager
from app.user.domain.models.user import User
from app.user.domain.services.user_service import UserService
from app.user.presentation.schemas.user import UserCreateSchema, UserOutSchema, UserUpdateSchema


router = APIRouter()


@router.post("/")
def create_user(payload: UserCreateSchema, service: UserService = Depends(get_user_service), shared_manager=Depends(get_shared_manager)):
    user_id = uuid4()
    with shared_manager.get_session(entity_id=user_id) as db:
        service.create(username=payload.username, user_id=user_id,  db=db)
    return {"message": "User created"}

@router.get("/{user_id}", response_model=UserOutSchema)
def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service), shared_manager=Depends(get_shared_manager)):
    with shared_manager.get_session(entity_id=user_id) as db:
        user: User = service.get_by_id(user_id, db=db)
    
    return user

@router.put("/{user_id}", response_model=UserOutSchema)
def update_user(user_id: UUID, payload: UserUpdateSchema, service: UserService = Depends(get_user_service), shared_manager=Depends(get_shared_manager)):
    with shared_manager.get_session(entity_id=user_id) as db:
        updated_user: User = service.update(user_id=user_id, data=payload.model_dump(), db=db)
    
    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service), shared_manager=Depends(get_shared_manager)):
    with shared_manager.get_session(entity_id=user_id) as db:
        service.delete(user_id=user_id, db=db)
    return {"message": "User deleted"}