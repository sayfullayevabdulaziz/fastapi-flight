from __future__ import annotations

import uuid
from io import BytesIO

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.crud.base import CRUDBase
from app.models.hotel import Hotel, AvailableRoom
from app.schemas import media_schema
from app.schemas.hotel_schema import IHotelCreateSchema, IHotelUpdatePartialSchema
from app.utils.minio_client import MinioClient
from app.utils.modify_media import get_filename_and_extension


class CRUDHotel(CRUDBase[Hotel, IHotelCreateSchema, IHotelUpdatePartialSchema]):

    @staticmethod
    async def add_media_files(hotel: Hotel, media_files: list, minio_client: MinioClient, db_session: AsyncSession):
        for media_data in media_files:
            old_filename, file_ext = get_filename_and_extension(media_data.filename)
            filename = f"{uuid.uuid4()}{file_ext}"
            file_content = await media_data.read()

            data_file = minio_client.put_object(
                file_path=f"hotels/images/{filename}",
                file_data=BytesIO(file_content),
                content_type=media_data.content_type,
            )

            data = media_schema.IMediaCreateSchema(filename=media_data.filename,
                                                   size=media_data.size,
                                                   path=data_file.file_name,
                                                   file_format=media_data.content_type,
                                                   )
            media_obj = await crud.media.create(obj_in=data, db_session=db_session)

            # obj = HotelMedia()
            # obj.hotel_image = hotel
            # obj.media = media_obj
            media_obj.hotels = hotel

            db_session.add(media_obj)
            await db_session.commit()
            await db_session.refresh(media_obj)

    async def create_with_media(self,
                                obj_in: IHotelCreateSchema,
                                media_files: list,
                                minio_client: MinioClient,
                                db_session: AsyncSession) -> Hotel:
        hotel = await self.create(obj_in=obj_in, db_session=db_session)

        # add media files
        await self.add_media_files(hotel, media_files, minio_client, db_session)

        return hotel

    async def get_filtered_hotels(self, rooms: list, db_session: AsyncSession):
        hotels = []
        for room in rooms:
            stmt = select(Hotel).join(AvailableRoom).where(AvailableRoom.id == room.id)
            response = await db_session.execute(stmt)
            # return response
            hotels.append(response.scalar_one_or_none())
        return hotels


hotel = CRUDHotel(Hotel)
