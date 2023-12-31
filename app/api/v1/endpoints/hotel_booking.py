from __future__ import annotations

from datetime import datetime, date

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.models import Hotel, AvailableRoom
from app.models.user import User
from app.schemas.hotel_booking_schema import (
    AHotelUserBookingReadSchema,
    AHotelUserBookingCreateSchema
)
from app.schemas.hotel_schema import IHotelReadSchema

router = APIRouter()


@router.post('/hotel-booking', status_code=status.HTTP_201_CREATED)
async def create_hotel_booking(
        new_booking: AHotelUserBookingCreateSchema,
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
):
    hotel_booking = await crud.hotel_user_booking.create_booking(obj_in=new_booking,
                                                                 created_by_id=current_user.id,
                                                                 )

    return AHotelUserBookingReadSchema.model_validate(hotel_booking)


@router.get('/get-hotels')
async def get_filtering_hotels(check_in: date, check_out: date,
                               db_session: AsyncSession = Depends(deps.get_db)
) -> list[IHotelReadSchema]:
    get_rooms = await crud.hotel_user_booking.get_booking(check_in=check_in, check_out=check_out)

    get_hotels = await crud.hotel.get_filtered_hotels(get_rooms, db_session)
    print(get_hotels, 'A21312')
    # print(get_rooms, 'a12321')
    # for room in get_rooms:
    #     print(room.hotel_room, room.id)

    return [IHotelReadSchema.model_validate(hotel) for hotel in get_hotels]

