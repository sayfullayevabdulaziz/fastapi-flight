from __future__ import annotations
from fastapi import (
    APIRouter,
    Depends,
    status, Query,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.deps import debit_deps
from app.models import DebitCard
from app.models.user import User
from app.schemas.debit_schema import ADebitCardReadSchema, ADebitCardCreateSchema, ADebitCardUpdatePartialSchema

router = APIRouter()


@router.get("/list")
async def read_debit_list(
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[ADebitCardReadSchema]:
    debit_cards = await crud.amenity.get_multi_ordered(order_by="id", db_session=db_session)
    return [ADebitCardReadSchema.model_validate(debit_card) for debit_card in debit_cards]


@router.get("/{user_id}/list")
async def read_available_room_list(
        user_id: int,
        order_by: str | None = Query(default='created_at'),
        desc: bool | None = Query(default=True),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[ADebitCardReadSchema]:
    debit_cards = await crud.debit_card.get_list(order_by=order_by, desc=desc,
                                                 where={DebitCard.user_id: user_id},
                                                 db_session=db_session)
    return [ADebitCardReadSchema.model_validate(debit_card) for debit_card in debit_cards]


@router.get("/{debit_id}")
async def get_debit_by_id(
        debit_card: ADebitCardReadSchema = Depends(debit_deps.is_valid_debit),
        current_user: User = Depends(
            deps.get_current_user()),

) -> ADebitCardReadSchema:
    return debit_card


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_debit_card(
        new_debit: ADebitCardCreateSchema,
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db)
) -> ADebitCardReadSchema:
    """
    Creates a new debit card
    """

    debit_card = await crud.debit_card.create(obj_in=new_debit, db_session=db_session)

    return debit_card


@router.put("/{debit_id}", status_code=status.HTTP_200_OK)
async def update_debit_card(
        payload: ADebitCardUpdatePartialSchema,
        debit_id: int = Depends(debit_deps.is_exist_debit),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> ADebitCardReadSchema:
    """
        Updates a debit card by id
    """
    debit_card = await crud.debit_card.update(obj_current=debit_id, obj_new=payload, db_session=db_session)
    return debit_card


@router.delete("/{debit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_debit_card(
        debit_id: int = Depends(debit_deps.is_valid_debit_id),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
):
    """
    Deletes an debit card by id
    """

    await crud.debit_card.remove(id=debit_id, db_session=db_session)

# =============== Front Part =======================
# Your all codes for Front Part
