from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.crud.base import CRUDBase
from app.models.hotel import AvailableRoom, Amenity, Freebie
from app.schemas.available_room_schema import AAvailableRoomCreateSchema, AAvailableRoomUpdateSchema
from app.utils.exceptions import IdNotFoundException


class CRUDAvailableRoom(CRUDBase[AvailableRoom, AAvailableRoomCreateSchema, AAvailableRoomUpdateSchema]):
    @staticmethod
    async def add_amenities_to_room(room: AvailableRoom, amenities: list, db_session):
        for amenity_id in amenities:
            amenity = await crud.amenity.get(id=amenity_id, db_session=db_session)

            if not amenity:
                raise IdNotFoundException(Amenity, id=amenity_id)

            room.amenities.append(amenity)
            db_session.add(room)
            await db_session.commit()
            await db_session.refresh(room)

    @staticmethod
    async def add_freebies_to_room(room: AvailableRoom, freebies: list, db_session):
        for freebie_id in freebies:
            freebie = await crud.freebie.get(id=freebie_id, db_session=db_session)

            if not freebie:
                raise IdNotFoundException(Freebie, id=freebie_id)

            room.freebies.append(freebie)
            db_session.add(room)
            await db_session.commit()
            await db_session.refresh(room)

    async def create_with_amenity_freebie(self,
                                          obj_in: AAvailableRoomCreateSchema,
                                          db_session: AsyncSession) -> AvailableRoom:
        available_room = await self.create(obj_in=obj_in, db_session=db_session)

        # add amenity to Room
        await self.add_amenities_to_room(available_room, obj_in.amenities, db_session)

        # add freebie to Room
        await self.add_freebies_to_room(available_room, obj_in.freebies, db_session)

        return available_room

available_room = CRUDAvailableRoom(AvailableRoom)
