from __future__ import annotations

from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.base import Base
from app.models.hotel import HotelRating
from app.schemas.hotel_rating_schema import AHotelRatingCreateSchema, AHotelRatingUpdateSchema

ModelType = TypeVar("ModelType", bound=Base)


class CRUDHotelRating(CRUDBase[HotelRating, AHotelRatingCreateSchema, AHotelRatingUpdateSchema]):
    async def create_rating(
            self,
            *,
            obj_in: AHotelRatingCreateSchema,
            user_id: int,
            db_session: AsyncSession
    ) -> ModelType:
        rating = HotelRating(**obj_in.model_dump())
        rating.user_id = user_id

        db_session.add(rating)
        await db_session.commit()

        return rating


hotel_rating = CRUDHotelRating(HotelRating)
