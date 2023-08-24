from pydantic import BaseModel, ConfigDict, Field, constr
from pydantic_partial import PartialModelMixin


class BaseDebitCardSchema(BaseModel):
    user_id: int
    card_number: str = Field(max_length=16)
    expired_date: str
    cvc: str
    name_on_card: str
    country: str
    is_active: bool = Field(default=True)


# =============== Admin Part =======================
class ADebitCardCreateSchema(BaseDebitCardSchema):
    pass


# This model will never be used.
class ADebitCardUpdateSchema(PartialModelMixin, BaseDebitCardSchema):
    pass


ADebitCardUpdatePartialSchema = ADebitCardUpdateSchema.model_as_partial()


class ADebitCardReadSchema(BaseDebitCardSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IDebitCardReadSchema(BaseDebitCardSchema):
    model_config = ConfigDict(from_attributes=True)
