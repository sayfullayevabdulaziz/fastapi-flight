from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class Media(Base):
    filename: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=True)
    size: Mapped[int] = mapped_column(nullable=True)
    file_format: Mapped[int] = mapped_column(nullable=False)
