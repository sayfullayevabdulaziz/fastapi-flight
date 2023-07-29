import redis.asyncio as aioredis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from redis.asyncio import Redis

from app import crud
from app.core import security
from app.core.config import settings
from app.db.session import sessionmanager
from app.models.user import User
from app.schemas.common_schema import TokenType
from app.utils.token import get_valid_tokens

from sqlalchemy.ext.asyncio import AsyncSession

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_redis_client() -> Redis:
    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis


def get_current_user():
    async def current_user(
            token: str = Depends(reusable_oauth2),
            redis_client: Redis = Depends(get_redis_client),
            db_session: AsyncSession = Depends(get_db)
    ) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user_id = int(payload["sub"])
        valid_access_tokens = await get_valid_tokens(
            redis_client, user_id, TokenType.ACCESS
        )
        if valid_access_tokens and token not in valid_access_tokens:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user: User = await crud.user.get(id=user_id, db_session=db_session)
        # print(user, "AAAAAAAAAAAAaaaaaaaa")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        # if required_roles:
        #     is_valid_role = False
        #     for role in required_roles:
        #         if role == user.role.name:
        #             is_valid_role = True
        #
        #     if not is_valid_role:
        #         raise HTTPException(
        #             status_code=403,
        #             detail=f"""Role "{required_roles}" is required for this action""",
        #         )

        return user

    return current_user


async def get_db():
    async with sessionmanager.session() as session:
        yield session
