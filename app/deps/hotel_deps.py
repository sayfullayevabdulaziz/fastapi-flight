from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app import crud
from app.api import deps
from app.models.hotel import Hotel
from app.schemas.hotel_schema import IHotelReadSchema
from app.utils.exceptions import IdNotFoundException


async def is_valid_hotel(
        hotel_id: Annotated[int, Path(title="The hotel_id of the hotel")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> IHotelReadSchema:
    hotel = await crud.hotel.get(id=hotel_id, db_session=db_session)

    if not hotel:
        raise IdNotFoundException(Hotel, id=hotel_id)

    return hotel