from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_async_sqlalchemy import db
from app import crud
from app.crud.base import CRUDBase
from app.models.hotel import HotelUserBooking, AvailableRoom, Hotel, Amenity
from app.schemas.hotel_booking_schema import AHotelUserBookingCreateSchema, AHotelUserBookingUpdateSchema
from app.utils.exceptions import IdNotFoundException


class CRUDHotelUserBooking(CRUDBase[HotelUserBooking, AHotelUserBookingCreateSchema, AHotelUserBookingUpdateSchema]):

    async def create_booking(self,
                             obj_in: AHotelUserBookingCreateSchema,
                             created_by_id: int,
                             db_session: AsyncSession | None = None):
        db_session = db.session or db_session

        available_room = await crud.available_room.get(id=obj_in.available_room_id, db_session=db_session)

        if not available_room:
            raise IdNotFoundException(AvailableRoom, id=obj_in.available_room_id)
        # obj_in.__setattr__('user_id', created_by_id)
        db_obj = self.model(**obj_in.model_dump())
        db_obj.user_id = created_by_id
        # db_obj = await self.create(obj_in=obj_in, db_session=db_session)

        db_session.add(db_obj)
        await db_session.commit()
        # await db_session.refresh(db_obj)

        return db_obj

    async def get_booking(self,
                          check_in: date,
                          check_out: date):
        db_session = db.session
        stmt = select(AvailableRoom) \
            .join(Hotel) \
            .where(Hotel.address.ilike("%Istanbul%")) \
            .where(AvailableRoom.price.between(0, 100000)) \
            .where(~AvailableRoom.user_room_booking.any(
                (HotelUserBooking.started_at < check_out) & (HotelUserBooking.stopped_at > check_in))
                   )
        #             .where(AvailableRoom.amenities.any(Amenity.name.in_([]))) \
        # stmt = select(Hotel).join_from(Hotel, subq)
        # .having(Hotel.address.ilike("%Istanbul%"))
        print("BU stmt", stmt)

        # stmt = select(AvailableRoom).outerjoin(HotelUserBooking, and_(
        #     AvailableRoom.id == HotelUserBooking.available_room_id,
        #     or_(
        #         HotelUserBooking.started_at <= check_in,
        #         HotelUserBooking.stopped_at >= check_out,
        #         and_(HotelUserBooking.started_at >= check_in, HotelUserBooking.started_at <= check_out),
        #     )
        # )).where(HotelUserBooking.id.is_(None))

        # stmt = select(self.model).filter(~or_(HotelUserBooking.started_at <= check_out),
        #                                      (HotelUserBooking.stopped_at >= check_in))

        response = await db_session.execute(stmt)
        # return response
        return response.scalars().all()


hotel_user_booking = CRUDHotelUserBooking(HotelUserBooking)
