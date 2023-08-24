from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app import crud
from app.api import deps
from app.models.hotel import AvailableRoom
from app.schemas.available_room_schema import AAvailableRoomReadSchema
from app.utils.exceptions import IdNotFoundException


async def is_exist_available(
        available_room_id: Annotated[int, Path(title="The available_room_id of the AvailableRoom")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> AvailableRoom:
    available_room = await crud.available_room.get(id=available_room_id, db_session=db_session)

    if not available_room:
        raise IdNotFoundException(AvailableRoom, id=available_room_id)

    return available_room


async def is_valid_available(
        available_room_id: Annotated[int, Path(title="The available_room_id of the AvailableRoom")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> AAvailableRoomReadSchema:
    available_room = await crud.available_room.get(id=available_room_id, db_session=db_session)

    if not available_room:
        raise IdNotFoundException(AvailableRoom, id=available_room_id)

    return available_room


async def is_valid_available_id(
        available_room_id: Annotated[int, Path(title="The available_room_id of the AvailableRoom")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> int:
    available_room = await crud.available_room.get(id=available_room_id, db_session=db_session)

    if not available_room:
        raise IdNotFoundException(AvailableRoom, id=available_room_id)

    return available_room_id
