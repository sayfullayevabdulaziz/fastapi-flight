from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Media(Base):
    filename: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=True)
    size: Mapped[int] = mapped_column(nullable=True)
    file_format: Mapped[str] = mapped_column(nullable=False)

    hotels: Mapped["Hotel"] = relationship(back_populates="images", secondary="link_hotel_media", lazy="joined")