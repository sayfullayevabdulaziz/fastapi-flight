from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.hotel import AvailableRoom
from app.schemas.available_room_schema import AAvailableRoomCreateSchema, AAvailableRoomUpdateSchema


class CRUDAvailableRoom(CRUDBase[AvailableRoom, AAvailableRoomCreateSchema, AAvailableRoomUpdateSchema]):
    pass


available_room = CRUDAvailableRoom(AvailableRoom)
