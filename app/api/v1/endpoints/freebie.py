from __future__ import annotations
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.deps import freebie_deps
from app.models.user import User
from app.schemas.freebie_schema import AFreebieReadSchema, AFreebieCreateSchema, AFreebieUpdateSchema


router = APIRouter()


@router.get("/list")
async def read_freebie_list(
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[AFreebieReadSchema]:
    freebies = await crud.freebie.get_multi_ordered(order_by="id", db_session=db_session)
    return [AFreebieReadSchema.model_validate(freebie) for freebie in freebies]


@router.get("/{freebie_id}")
async def get_freebie_by_id(
        freebie: AFreebieReadSchema = Depends(freebie_deps.is_valid_freebie),
        current_user: User = Depends(
            deps.get_current_user()),

) -> AFreebieReadSchema:
    return freebie


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_freebie(
        new_freebie: AFreebieCreateSchema,
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db)
) -> AFreebieReadSchema:
    """
    Creates a new freebie
    """

    freebie = await crud.freebie.create(obj_in=new_freebie, db_session=db_session)

    return freebie


@router.put("/{freebie_id}", status_code=status.HTTP_200_OK)
async def update_freebie(
        payload: AFreebieUpdateSchema,
        freebie_id: int = Depends(freebie_deps.is_exist_freebie),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> AFreebieReadSchema:
    """
        Updates a freebie by id
    """
    freebie = await crud.freebie.update(obj_current=freebie_id, obj_new=payload, db_session=db_session)
    return freebie


@router.delete("/{freebie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_freebie(
        freebie_id: int = Depends(freebie_deps.is_valid_freebie_id),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
):
    """
    Deletes a freebie by id
    """

    await crud.freebie.remove(id=freebie_id, db_session=db_session)

# =============== Front Part =======================
# Your all codes for Front Part
