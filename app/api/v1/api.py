from fastapi import APIRouter
from app.api.v1.endpoints import (
    user,
    login,
    user_site
)

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(user_site.router, prefix="/site", tags=["User Site"])
