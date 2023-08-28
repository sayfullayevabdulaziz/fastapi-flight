from __future__ import annotations

import datetime
from typing import Any
from dateutil.parser import parse
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_partial import PartialModelMixin


class BaseHotelUserBookingSchema(BaseModel):
    available_room_id: int
    started_at: datetime.date = Field(default=datetime.date.today)
    stopped_at: datetime.date = Field(default=datetime.date.today)


# =============== Admin Part =======================
class AHotelUserBookingCreateSchema(BaseHotelUserBookingSchema):
    # user_id: int | None = None

    @model_validator(mode='before')
    @classmethod
    def check_datetime_difference(cls, data: Any):
        start = parse(data['started_at'])
        stop = parse(data['stopped_at'])
        if isinstance(start, datetime.datetime):
            if start > stop:
                raise ValueError("The stopped_at field must be greater-or-equal than the started_at field")
        elif isinstance(stop, datetime.datetime):
            if stop < start:
                raise ValueError("The stopped_at field must be greater-or-equal than the started_at field")
        return data


# This model will never be used.
class AHotelUserBookingUpdateSchema(PartialModelMixin, BaseHotelUserBookingSchema):
    pass


AHotelUserBookingUpdatePartialSchema = AHotelUserBookingUpdateSchema.model_as_partial()


class AHotelUserBookingReadSchema(BaseModel):
    available_room_id: int
    user_id: int
    started_at: datetime.date
    stopped_at: datetime.date

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IHotelUserBookingReadSchema(BaseHotelUserBookingSchema):
    model_config = ConfigDict(from_attributes=True)
