from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def test(user_id: str):
    a = hash(user_id)
    print(-5122704023163466000 %3)
    return {"hash_value":a, "div_mod": -5122704023163466000 %3}