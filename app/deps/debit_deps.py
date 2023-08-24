from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app import crud
from app.api import deps
from app.models.debit_card import DebitCard
from app.schemas.debit_schema import ADebitCardReadSchema
from app.utils.exceptions import IdNotFoundException


async def is_exist_debit(
        debit_id: Annotated[int, Path(title="The debit_id of the Debit Card")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> DebitCard:
    debit_card = await crud.debit_card.get(id=debit_id, db_session=db_session)

    if not debit_card:
        raise IdNotFoundException(DebitCard, id=debit_id)

    return debit_card


async def is_valid_debit(
        debit_id: Annotated[int, Path(title="The debit_id of the DebitCard")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> ADebitCardReadSchema:
    debit_card = await crud.debit_card.get(id=debit_id, db_session=db_session)

    if not debit_card:
        raise IdNotFoundException(DebitCard, id=debit_id)

    return debit_card


async def is_valid_debit_id(
        debit_id: Annotated[int, Path(title="The debit_id of the DebitCard")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> int:
    debit_card = await crud.debit_card.get(id=debit_id, db_session=db_session)

    if not debit_card:
        raise IdNotFoundException(DebitCard, id=debit_id)

    return debit_id
