from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app import crud
from app.api import deps
from app.models.hotel import Freebie
from app.schemas.freebie_schema import AFreebieReadSchema
from app.utils.exceptions import IdNotFoundException


async def is_exist_freebie(
        freebie_id: Annotated[int, Path(title="The freebie_id of the freebie")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> Freebie:
    freebie = await crud.freebie.get(id=freebie_id, db_session=db_session)

    if not freebie:
        raise IdNotFoundException(Freebie, id=freebie_id)

    return freebie


async def is_valid_freebie(
        freebie_id: Annotated[int, Path(title="The freebie_id of the freebie")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> AFreebieReadSchema:
    freebie = await crud.freebie.get(id=freebie_id, db_session=db_session)

    if not freebie:
        raise IdNotFoundException(Freebie, id=freebie_id)

    return freebie


async def is_valid_freebie_id(
        freebie_id: Annotated[int, Path(title="The freebie_id of the freebie")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> int:
    freebie = await crud.freebie.get(id=freebie_id, db_session=db_session)

    if not freebie:
        raise IdNotFoundException(Freebie, id=freebie_id)

    return freebie_id
