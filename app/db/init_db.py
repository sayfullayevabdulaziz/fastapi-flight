from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from app import crud

from app.core.config import settings
from app.schemas.user import IUserCreateSchema


user: dict[str, IUserCreateSchema] = {
    "data": IUserCreateSchema(
        first_name="Abdulaziz",
        last_name="Sayfullayev",
        password=settings.FIRST_SUPERUSER_PASSWORD,
        confirm_password=settings.FIRST_SUPERUSER_PASSWORD,
        phone='998903470113',
        email=settings.FIRST_SUPERUSER_EMAIL,
        is_superuser=True,
    )
}


async def init_db(db_session: AsyncSession) -> None:
    current_user = await crud.user.get_by_email(
        email=user["data"].email, db_session=db_session
    )

    if not current_user:
        await crud.user.create(obj_in=user["data"], db_session=db_session)
