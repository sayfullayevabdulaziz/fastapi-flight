from pydantic import BaseModel, ConfigDict


class BaseAmenitySchema(BaseModel):
    name: str


# =============== Admin Part =======================
class AAmenityCreateSchema(BaseAmenitySchema):
    pass


# This model will never be used.
class AAmenityUpdateSchema(BaseAmenitySchema):
    pass


class AAmenityReadSchema(BaseAmenitySchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IAmenityReadSchema(BaseAmenitySchema):
    model_config = ConfigDict(from_attributes=True)
