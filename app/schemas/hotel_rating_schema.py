from pydantic import BaseModel, ConfigDict, Field


class BaseHotelRatingSchema(BaseModel):
    hotel_id: int
    comment: str
    rating: int = Field(default=0, ge=0, le=5)


# =============== Admin Part =======================
class AHotelRatingCreateSchema(BaseHotelRatingSchema):
    pass


# This model will never be used.
class AHotelRatingUpdateSchema(BaseHotelRatingSchema):
    pass


class AHotelRatingReadSchema(BaseHotelRatingSchema):
    # id: int

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IHotelRatingReadSchema(BaseHotelRatingSchema):
    model_config = ConfigDict(from_attributes=True)
