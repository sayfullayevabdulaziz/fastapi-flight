from __future__ import annotations

from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.hotel_rating_schema import (
    AHotelRatingCreateSchema,
    AHotelRatingReadSchema
)

router = APIRouter()


@router.post('/hotel-rating', status_code=status.HTTP_201_CREATED)
async def create_hotel_rating(
        new_booking: AHotelRatingCreateSchema,
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> AHotelRatingReadSchema:
    hotel_rating = await crud.hotel_rating.create_rating(obj_in=new_booking,
                                                         user_id=current_user.id,
                                                         db_session=db_session
                                                         )

    print(hotel_rating, "Aaaaaaaaaaw23")

    return hotel_rating
