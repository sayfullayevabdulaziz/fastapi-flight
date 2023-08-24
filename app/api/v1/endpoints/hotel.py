from __future__ import annotations
from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File
)


from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.api.deps import minio_auth
from app.deps import hotel_deps
from app.models.user import User
from app.schemas.hotel_schema import IHotelReadSchema, IHotelCreateSchema
from app.utils.minio_client import MinioClient

router = APIRouter()


@router.get("/list")
async def read_hotel_list(
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
) -> list[IHotelReadSchema]:
    hotels = await crud.hotel.get_multi_ordered(order_by="id", db_session=db_session)
    return [IHotelReadSchema.model_validate(hotel) for hotel in hotels]


# @router.get("/order_by_created_at")
# async def get_user_list_order_by_created_at(
#         current_user: User = Depends(
#             deps.get_current_user()
#         ),
#         db_session: AsyncSession = Depends(deps.get_db),
# ) -> list[IUserReadSchema]:
#     users = await crud.user.get_multi_ordered(
#         order_by="created_at", db_session=db_session
#     )
#     return [IUserReadSchema.model_validate(user) for user in users]


@router.get("/{hotel_id}")
async def get_hotel_by_id(
        hotel: IHotelReadSchema = Depends(hotel_deps.is_valid_hotel),
        current_user: User = Depends(
            deps.get_current_user()),

) -> IHotelReadSchema:

    return hotel


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_hotel(
        new_hotel: IHotelCreateSchema,
        media_files: list[UploadFile] = File(),
        current_user: User = Depends(
            deps.get_current_user()
        ),
        db_session: AsyncSession = Depends(deps.get_db),
        minio_client: MinioClient = Depends(minio_auth)
) -> IHotelReadSchema:
    """
    Creates a new hotel
    """
    # new_hotel = IHotelCreateSchema(name=name, short_description=short_description, description=description,
    #                                address=address, location=location, is_active=is_active, is_recommend=is_recommend)

    hotel = await crud.hotel.create_with_media(obj_in=new_hotel,
                                               media_files=media_files,
                                               minio_client=minio_client,
                                               db_session=db_session)

    return IHotelReadSchema.model_validate(hotel)


# @router.put("/{user_id}", status_code=status.HTTP_200_OK)
# async def update_user(
#         payload: IUserUpdatePartialSchema,
#         user_id: int = Depends(user_deps.is_valid_user),
#         current_user: User = Depends(
#             deps.get_current_user()
#         ),
#         db_session: AsyncSession = Depends(deps.get_db),
# ) -> IUserReadSchema:
#     """
#         Updates a user by his/her id
#     """
#     user = await crud.user.update(obj_current=user_id, obj_new=payload, db_session=db_session)
#     return IUserReadSchema.model_validate(user)
#
#
# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def remove_user(
#         user_id: int = Depends(user_deps.is_valid_user_id),
#         current_user: User = Depends(
#             deps.get_current_user()
#         ),
#         db_session: AsyncSession = Depends(deps.get_db),
# ):
#     """
#     Deletes a user by his/her id
#     """
#     if current_user.id == user_id:
#         raise UserSelfDeleteException()
#
#     await crud.user.remove(id=user_id, db_session=db_session)


#       name: str = Form(...),
#         short_description: str = Form(...),
#         description: str = Form(...),
#         address: str = Form(..., ),
#         location: str = Form(..., ),
#         is_active: bool | None = Form(default=True,),
#         is_recommend: bool | None = Form(default=True, ),