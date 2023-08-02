from fastapi import APIRouter


user_router = APIRouter()


@user_router.get("/")
def read_root():
    return {"Hello": "World"}
