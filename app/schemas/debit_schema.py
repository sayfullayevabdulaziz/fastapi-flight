from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_partial import PartialModelMixin
from pydantic_extra_types.payment import PaymentCardBrand, PaymentCardNumber


class BaseDebitCardSchema(BaseModel):
    user_id: int
    card_number: PaymentCardNumber
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


class ADebitCardReadSchema(BaseModel):
    id: int
    card_number: PaymentCardNumber
    expired_date: str

    @field_validator('card_number', mode='after')
    @classmethod
    def card_last4(cls, v: str) -> str:
        return PaymentCardNumber(v).last4

    model_config = ConfigDict(from_attributes=True)


# =============== Front Part =======================

class IDebitCardReadSchema(BaseDebitCardSchema):
    model_config = ConfigDict(from_attributes=True)
