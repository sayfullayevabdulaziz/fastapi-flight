from pydantic import BaseModel, ConfigDict, Field
from pydantic_partial import PartialModelMixin


class BaseAvailableRoomSchema(BaseModel):
    hotel_id: int
    name: str
    price: int = Field(default=0)
    view: str
    bed: str


# =============== Admin Part =======================
class AAvailableRoomCreateSchema(BaseAvailableRoomSchema):
    pass


# This model will never be used.
class AAvailableRoomUpdateSchema(PartialModelMixin, BaseAvailableRoomSchema):
    pass


AAvailableRoomUpdatePartialSchema = AAvailableRoomUpdateSchema.model_as_partial()


class AAvailableRoomReadSchema(BaseAvailableRoomSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IAvailableRoomReadSchema(BaseAvailableRoomSchema):
    model_config = ConfigDict(from_attributes=True)
