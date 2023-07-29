from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    status,
    Body,
    HTTPException
)
from pydantic import EmailStr
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.api.deps import get_redis_client
from app.api.v1.celery_tasks import send_code_email
from app.core import security
from app.core.config import settings
from app.deps import user_deps
from app.schemas.common_schema import TokenType
from app.schemas.token_schema import Token
from app.schemas.user import ReadRegisterUserSchema, RegisterUserSchema, UserEmailSchema, SetNewPasswordSchema
from app.utils.code_generate import generate_code, add_code_to_redis, get_valid_code
from app.utils.token import delete_tokens, add_token_to_redis

router = APIRouter()


@router.post("/forgot-password")
async def user_forgot_password(
        check_email: UserEmailSchema = Depends(user_deps.user_forgot_password),
        redis_client: Redis = Depends(get_redis_client),
):
    code = generate_code()

    email_to = check_email.email

    await add_code_to_redis(redis_client, email_to, code)

    result = send_code_email.apply_async([email_to, code])

    return {"task_id": result.id, "status": status.HTTP_200_OK}


@router.post("/change_password")
async def change_password(
        new_password: SetNewPasswordSchema,
        email: EmailStr = Body(),
        redis_client: Redis = Depends(get_redis_client),
        db_session: AsyncSession = Depends(deps.get_db)
) -> Token:
    """
    Change password
    """
    user = await crud.user.get_by_email(email=email, db_session=db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not found",
        )

    new_hashed_password = security.get_password_hash(new_password.password)
    await crud.user.update(
        obj_current=user, obj_new={"hashed_password": new_hashed_password},
        db_session=db_session
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        user.id, expires_delta=refresh_token_expires
    )
    data = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
    )

    await delete_tokens(redis_client, user, TokenType.ACCESS)
    await delete_tokens(redis_client, user, TokenType.REFRESH)
    await add_token_to_redis(
        redis_client,
        user,
        access_token,
        TokenType.ACCESS,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    await add_token_to_redis(
        redis_client,
        user,
        refresh_token,
        TokenType.REFRESH,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )

    return data


@router.post("/register")
async def user_register(
        new_user: RegisterUserSchema = Depends(user_deps.register_user_exists),
        db_session: AsyncSession = Depends(deps.get_db),
) -> ReadRegisterUserSchema:
    user = await crud.user.create(obj_in=new_user, db_session=db_session)
    return ReadRegisterUserSchema.model_validate(user)


@router.post("/check-code")
async def check_verification_code(
        email: EmailStr = Body(),
        code: int = Body(description="Verification code"),
        redis_client: Redis = Depends(get_redis_client),
):
    check_code = await get_valid_code(redis_client, email, code)
    if not check_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The verification code is incorrect!")
    return {"status": status.HTTP_200_OK}
