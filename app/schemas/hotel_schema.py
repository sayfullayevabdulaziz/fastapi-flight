from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_partial import PartialModelMixin

from app.schemas.amenity_schema import IAmenityReadSchema
from app.schemas.available_room_schema import AAvailableRoomReadSchema
from app.schemas.media_schema import IMediaReadSchema


class IHotelBaseSchema(BaseModel):
    name: str
    short_description: str
    description: str
    address: str
    location: str
    is_active: bool | None = Field(default=True)
    is_recommend: bool | None = Field(default=True)


class IHotelCreateSchema(IHotelBaseSchema):
    amenities: list[int] = Field(exclude=True)
    freebies: list[int] = Field(exclude=True)

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)


# All these fields are optional
class IHotelUpdateSchema(PartialModelMixin, IHotelBaseSchema):
    pass


IHotelUpdatePartialSchema = IHotelUpdateSchema.model_as_partial()


class IHotelReadSchema(IHotelBaseSchema):
    id: int
    images: list[IMediaReadSchema]
    sum_rating: float
    amenities: list[IAmenityReadSchema]
    available_rooms: list[AAvailableRoomReadSchema]
    model_config = ConfigDict(from_attributes=True)
