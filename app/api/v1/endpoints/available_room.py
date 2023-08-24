from __future__ import annotations
from fastapi import (
    APIRouter,
    Depends,
    status, Query,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.deps import available_deps
from app.models import AvailableRoom
from app.models.user import User
from app.schemas.available_room_schema import (
    AAvailableRoomReadSchema,
    AAvailableRoomCreateSchema,
    AAvailableRoomUpdatePartialSchema
)

router = APIRouter()


@router.get("/{hotel_id}/list")
async def read_available_room_list(
        hotel_id: int,
        order_by: str | None = Query(default='created_at'),
        desc: bool | None = Query(default=True),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[AAvailableRoomReadSchema]:
    available_rooms = await crud.available_room.get_list(order_by=order_by, desc=desc,
                                                         where={AvailableRoom.hotel_id: hotel_id},
                                                         db_session=db_session)
    return [AAvailableRoomReadSchema.model_validate(available) for available in available_rooms]


@router.get("/{available_room_id}")
async def get_available_by_id(
        available_room: AAvailableRoomReadSchema = Depends(available_deps.is_valid_available),
        current_user: User = Depends(
            deps.get_current_user()),

) -> AAvailableRoomReadSchema:
    return available_room


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_freebie(
        new_available: AAvailableRoomCreateSchema,
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db)
) -> AAvailableRoomReadSchema:
    """
    Creates a new available_room
    """

    available_room = await crud.available_room.create(obj_in=new_available, db_session=db_session)

    return available_room


@router.put("/{available_room_id}", status_code=status.HTTP_200_OK)
async def update_freebie(
        payload: AAvailableRoomUpdatePartialSchema,
        available_room_id: int = Depends(available_deps.is_exist_available),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> AAvailableRoomReadSchema:
    """
        Updates a freebie by id
    """
    available_room = await crud.available_room.update(obj_current=available_room_id, obj_new=payload,
                                                      db_session=db_session)
    return available_room


@router.delete("/{available_room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_available_room(
        available_room_id: int = Depends(available_deps.is_valid_available_id),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
):
    """
    Deletes an available room id by id
    """

    await crud.available_room.remove(id=available_room_id, db_session=db_session)

# =============== Front Part =======================
# Your all codes for Front Part
