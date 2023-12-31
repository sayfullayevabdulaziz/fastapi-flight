from typing import List
from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, validates, relationship
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class User(Base):
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column(nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    credit_cards: Mapped[List["DebitCard"]] = relationship(backref='user_cards')
    hotel_booking: Mapped[List["AvailableRoom"]] = relationship(secondary='hotel_user_booking',
                                                                back_populates='user_room_booking')

    @validates("email")
    def validate_email(self, key, address: str):
        if '@' not in address:
            raise ValueError("Email xato kiritildi")
        return address
