from fastapi import HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.user import IUserCreateSchema, IUserReadSchema, UserEmailSchema, RegisterUserSchema
from app.utils.exceptions import IdNotFoundException


async def user_exists(new_user: IUserCreateSchema,
                      db_session: AsyncSession = Depends(deps.get_db)) -> IUserCreateSchema:
    user = await crud.user.get_by_email(email=new_user.email, db_session=db_session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a user with same email",
        )

    return new_user


async def register_user_exists(new_user: RegisterUserSchema,
                               db_session: AsyncSession = Depends(deps.get_db)) -> RegisterUserSchema:
    user = await crud.user.get_by_email(email=new_user.email, db_session=db_session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a user with same email",
        )

    return new_user


async def user_forgot_password(check_email: UserEmailSchema,
                               db_session: AsyncSession = Depends(deps.get_db)) -> UserEmailSchema:
    user = await crud.user.get_by_email(email=check_email.email, db_session=db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email not found",
        )
    return check_email


async def is_valid_user(
        user_id: Annotated[int, Path(title="The user_id of the user")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> IUserReadSchema:
    user = await crud.user.get(id=user_id, db_session=db_session)
    if not user:
        raise IdNotFoundException(User, id=user_id)

    return user


async def is_valid_user_id(
        user_id: Annotated[int, Path(title="The user_id of the user")],
        db_session: AsyncSession = Depends(deps.get_db)
) -> int:
    user = await crud.user.get(id=user_id, db_session=db_session)
    if not user:
        raise IdNotFoundException(User, id=user_id)

    return user_id
