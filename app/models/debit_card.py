from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, validates
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class DebitCard(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    card_number: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    expired_date: Mapped[str] = mapped_column(nullable=False)
    cvc: Mapped[str] = mapped_column(nullable=False)
    name_on_card: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    @validates("card_number")
    def validate_card_number(self, key, card_number: str):
        if len(card_number) != 16:
            raise ValueError("The card number must be 16 digits.")
        return card_number
