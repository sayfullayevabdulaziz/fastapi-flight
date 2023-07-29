from __future__ import annotations

from pydantic import BaseModel, EmailStr, ConfigDict, Field, model_validator, StringConstraints
from pydantic_partial import PartialModelMixin
from typing_extensions import Annotated

PhoneStr = Annotated[str, StringConstraints(pattern=r'^998\d{9}$')]


class IUserBaseSchema(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr
    phone: PhoneStr = Field(default='998901234567')
    password: str
    confirm_password: str
    is_active: bool | None = Field(default=True)
    is_superuser: bool | None = Field(default=False)

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'IUserBaseSchema':
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self


class IUserCreateSchema(IUserBaseSchema):
    pass


# All these fields are optional
class IUserUpdateSchema(PartialModelMixin, IUserBaseSchema):
    pass


IUserUpdatePartialSchema = IUserUpdateSchema.model_as_partial()


class IUserReadSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    email: EmailStr
    phone: PhoneStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Site Schemas starts
class UserEmailSchema(BaseModel):
    email: EmailStr


class RegisterUserSchema(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr
    phone: PhoneStr = Field(default='998901234567')
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'RegisterUserSchema':
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self


class ReadRegisterUserSchema(BaseModel):
    first_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class SetNewPasswordSchema(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'SetPasswordSchema':
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self
