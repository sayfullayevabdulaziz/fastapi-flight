from pydantic import BaseModel, ConfigDict


class BaseFreebieSchema(BaseModel):
    name: str


# =============== Admin Part =======================
class AFreebieCreateSchema(BaseFreebieSchema):
    pass


# This model will never be used.
class AFreebieUpdateSchema(BaseFreebieSchema):
    pass


class AFreebieReadSchema(BaseFreebieSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IFreebieReadSchema(BaseFreebieSchema):
    model_config = ConfigDict(from_attributes=True)
