from __future__ import annotations

from pydantic.networks import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import IUserCreateSchema, IUserUpdateSchema


class CRUDUser(CRUDBase[User, IUserCreateSchema, IUserUpdateSchema]):
    async def get_by_email(
            self, *, email: str, db_session: AsyncSession
    ) -> User | None:
        users = await db_session.execute(select(User).where(User.email == email))
        return users.scalar_one_or_none()

    async def get_by_id_active(self, *, id: int, db_session: AsyncSession) -> User | None:
        user: User = await super().get(id=id, db_session=db_session)
        if not user:
            return None
        if user.is_active is False:
            return None

        return user

    async def authenticate(self, *, email: EmailStr, password: str, db_session: AsyncSession) -> User | None:
        user = await self.get_by_email(email=email, db_session=db_session)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def create(self, *, obj_in: IUserCreateSchema, created_by_id: int | str | None = None,
                     db_session: AsyncSession) -> User:

        db_obj = User(**obj_in.model_dump(exclude={'password', 'confirm_password'}))
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
