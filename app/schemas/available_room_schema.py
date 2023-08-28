from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic_partial import PartialModelMixin

from app.schemas.amenity_schema import AAmenityReadSchema
from app.schemas.freebie_schema import AFreebieReadSchema
from app.schemas.hotel_booking_schema import AHotelUserBookingReadSchema


class BaseAvailableRoomSchema(BaseModel):
    hotel_id: int
    name: str
    price: int = Field(default=0)
    view: str
    bed: int = Field(ge=1)
    is_active: bool = Field(default=True)


# =============== Admin Part =======================
class AAvailableRoomCreateSchema(BaseAvailableRoomSchema):
    amenities: list[int] = Field(exclude=True)
    freebies: list[int] = Field(exclude=True)


# This model will never be used.
class AAvailableRoomUpdateSchema(PartialModelMixin, BaseAvailableRoomSchema):
    pass


AAvailableRoomUpdatePartialSchema = AAvailableRoomUpdateSchema.model_as_partial()


class AAvailableRoomReadSchema(BaseAvailableRoomSchema):
    id: int
    amenities: list[AAmenityReadSchema]
    freebies: list[AFreebieReadSchema]
    # user_room_booking: list[AHotelUserBookingReadSchema]

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IAvailableRoomReadSchema(BaseAvailableRoomSchema):
    model_config = ConfigDict(from_attributes=True)
