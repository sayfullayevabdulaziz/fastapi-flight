from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.deps import user_deps
from app.models.user import User
from app.schemas.user import (
    IUserCreateSchema,
    IUserReadSchema,
    IUserUpdatePartialSchema
)
from app.utils.exceptions import (
    UserSelfDeleteException,
)

router = APIRouter()


@router.get("/list")
async def read_users_list(
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[IUserReadSchema]:
    users = await crud.user.get_multi_ordered(order_by="id", db_session=db_session)
    return [IUserReadSchema.model_validate(user) for user in users]


@router.get("/order_by_created_at")
async def get_user_list_order_by_created_at(
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[IUserReadSchema]:
    users = await crud.user.get_multi_ordered(
        order_by="created_at", db_session=db_session
    )
    return [IUserReadSchema.model_validate(user) for user in users]


@router.get("/{user_id}")
async def get_user_by_id(
        user: IUserReadSchema = Depends(user_deps.is_valid_user),
        current_user: User = Depends(
            deps.get_current_user()),

) -> IUserReadSchema:
    return user


@router.get("")
async def get_my_data(
        current_user: User = Depends(deps.get_current_user()),
) -> IUserReadSchema:
    """
    Gets my user profile information
    """
    return IUserReadSchema.model_validate(current_user)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
        new_user: IUserCreateSchema = Depends(user_deps.user_exists),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> IUserReadSchema:
    """
    Creates a new user
    """
    user = await crud.user.create(obj_in=new_user, db_session=db_session)
    return IUserReadSchema.model_validate(user)


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
        payload: IUserUpdatePartialSchema,
        user_id: int = Depends(user_deps.is_valid_user),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> IUserReadSchema:
    """
        Updates a user by his/her id
    """
    user = await crud.user.update(obj_current=user_id, obj_new=payload, db_session=db_session)
    return IUserReadSchema.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
        user_id: int = Depends(user_deps.is_valid_user_id),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
):
    """
    Deletes a user by his/her id
    """
    if current_user.id == user_id:
        raise UserSelfDeleteException()

    await crud.user.remove(id=user_id, db_session=db_session)
