from __future__ import annotations
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.deps import amenity_deps
from app.models.user import User
from app.schemas.amenity_schema import AAmenityReadSchema, AAmenityCreateSchema, AAmenityUpdateSchema


router = APIRouter()


@router.get("/list")
async def read_amenity_list(
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[AAmenityReadSchema]:
    amenities = await crud.amenity.get_multi_ordered(order_by="id", db_session=db_session)
    return [AAmenityReadSchema.model_validate(amenity) for amenity in amenities]


@router.get("/{amenity_id}")
async def get_amenity_by_id(
        amenity: AAmenityReadSchema = Depends(amenity_deps.is_valid_amenity),
        current_user: User = Depends(
            deps.get_current_user()),

) -> AAmenityReadSchema:
    return amenity


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_amenity(
        new_amenity: AAmenityCreateSchema,
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db)
) -> AAmenityReadSchema:
    """
    Creates a new amenity
    """

    amenity = await crud.amenity.create(obj_in=new_amenity, db_session=db_session)

    return amenity


@router.put("/{amenity_id}", status_code=status.HTTP_200_OK)
async def update_amenity(
        payload: AAmenityUpdateSchema,
        amenity_id: int = Depends(amenity_deps.is_exist_amenity),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> AAmenityReadSchema:
    """
        Updates an amenity by id
    """
    amenity = await crud.amenity.update(obj_current=amenity_id, obj_new=payload, db_session=db_session)
    return amenity


@router.delete("/{amenity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_amenity(
        amenity_id: int = Depends(amenity_deps.is_valid_amenity_id),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
):
    """
    Deletes an amenity by id
    """

    await crud.amenity.remove(id=amenity_id, db_session=db_session)

# =============== Front Part =======================
# Your all codes for Front Part
