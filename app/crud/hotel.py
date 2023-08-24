from __future__ import annotations
import uuid
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.crud.base import CRUDBase
from app.models.hotel import Hotel, Amenity, Freebie
from app.schemas import media_schema
from app.schemas.hotel_schema import IHotelCreateSchema, IHotelUpdatePartialSchema
from app.utils.exceptions import IdNotFoundException
from app.utils.minio_client import MinioClient
from app.utils.modify_media import get_filename_and_extension


class CRUDHotel(CRUDBase[Hotel, IHotelCreateSchema, IHotelUpdatePartialSchema]):

    @staticmethod
    async def add_amenities_to_hotel(hotel: Hotel, amenities: list, db_session):
        for amenity_id in amenities:
            amenity = await crud.amenity.get(id=amenity_id, db_session=db_session)

            if not amenity:
                raise IdNotFoundException(Amenity, id=amenity_id)

            hotel.amenities.append(amenity)
            db_session.add(hotel)
            await db_session.commit()
            await db_session.refresh(hotel)

    @staticmethod
    async def add_freebies_to_hotel(hotel: Hotel, freebies: list, db_session):
        for freebie_id in freebies:
            freebie = await crud.freebie.get(id=freebie_id, db_session=db_session)

            if not freebie:
                raise IdNotFoundException(Freebie, id=freebie_id)

            hotel.freebies.append(freebie)
            db_session.add(hotel)
            await db_session.commit()
            await db_session.refresh(hotel)

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

        # add amenities to hotel
        await self.add_amenities_to_hotel(hotel, obj_in.amenities, db_session)
        # add freebies to hotel
        await self.add_freebies_to_hotel(hotel, obj_in.freebies, db_session)
        # add media files
        await self.add_media_files(hotel, media_files, minio_client, db_session)

        return hotel


hotel = CRUDHotel(Hotel)
