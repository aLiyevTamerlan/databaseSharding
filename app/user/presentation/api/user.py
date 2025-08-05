from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def test(user_id: str):
    print(hash(user_id) %3)
    return True