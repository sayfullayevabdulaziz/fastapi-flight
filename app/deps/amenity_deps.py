from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app import crud
from app.api import deps
from app.models.hotel import Amenity
from app.schemas.amenity_schema import AAmenityReadSchema
from app.utils.exceptions import IdNotFoundException


async def is_exist_amenity(
        amenity_id: Annotated[int, Path(title="The amenity_id of the amenity")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> Amenity:
    amenity = await crud.amenity.get(id=amenity_id, db_session=db_session)

    if not amenity:
        raise IdNotFoundException(Amenity, id=amenity_id)

    return amenity


async def is_valid_amenity(
        amenity_id: Annotated[int, Path(title="The amenity_id of the amenity")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> AAmenityReadSchema:
    amenity = await crud.amenity.get(id=amenity_id, db_session=db_session)

    if not amenity:
        raise IdNotFoundException(Amenity, id=amenity_id)

    return amenity


async def is_valid_amenity_id(
        amenity_id: Annotated[int, Path(title="The amenity_id of the amenity")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> int:
    amenity = await crud.amenity.get(id=amenity_id, db_session=db_session)

    if not amenity:
        raise IdNotFoundException(Amenity, id=amenity_id)

    return amenity_id
