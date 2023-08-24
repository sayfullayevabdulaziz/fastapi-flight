from pydantic import BaseModel, ConfigDict


class IBaseMediaSchema(BaseModel):
    filename: str
    path: str
    size: int
    file_format: str


class IMediaCreateSchema(IBaseMediaSchema):
    pass


# This model will never be used.
class IMediaUpdateSchema(IBaseMediaSchema):
    pass


class IMediaReadSchema(IBaseMediaSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
