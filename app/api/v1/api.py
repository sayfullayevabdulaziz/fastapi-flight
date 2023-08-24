from fastapi import APIRouter
from app.api.v1.endpoints import (
    user,
    login,
    user_site,
    hotel,
    amenity,
    freebie,
    available_room,
    debit_card
)

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(user_site.router, prefix="/site", tags=["User Site"])
api_router.include_router(hotel.router, prefix="/hotel", tags=["Hotel"])
api_router.include_router(amenity.router, prefix="/amenity", tags=["Amenities"])
api_router.include_router(freebie.router, prefix="/freebie", tags=["Freebies"])
api_router.include_router(available_room.router, prefix="/available-room", tags=["Available Rooms"])
api_router.include_router(debit_card.router, prefix="/debit-card", tags=["Debit Cards"])
