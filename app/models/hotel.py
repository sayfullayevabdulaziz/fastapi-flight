import uuid
from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, validates
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, Date, CheckConstraint, and_, UniqueConstraint
from app.models.base import Base

# M2M tables
link_freebie_room = Table(
    "link_freebie_room",
    Base.metadata,
    Column("available_room_id", ForeignKey("available_room.id"), primary_key=True),
    Column("freebie_id", ForeignKey("freebie.id"), primary_key=True),
)

link_amenity_room = Table(
    "link_amenity_room",
    Base.metadata,
    Column("available_room_id", ForeignKey("available_room.id"), primary_key=True),
    Column("amenity_id", ForeignKey("amenity.id"), primary_key=True),
)

link_hotel_media = Table(
    "link_hotel_media",
    Base.metadata,
    Column("hotel_id", ForeignKey("hotel.id", ondelete="CASCADE"), primary_key=True),
    Column("media_id", ForeignKey("media.id"), primary_key=True),
)


class Hotel(Base):
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    short_description: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_recommend: Mapped[bool] = mapped_column(default=True)

    user_ratings: Mapped[List["HotelRating"]] = relationship(back_populates="hotel_ref", lazy="selectin")
    available_rooms: Mapped[List["AvailableRoom"]] = relationship(back_populates="hotel_room", lazy='selectin')
    images: Mapped[List["Media"]] = relationship(back_populates="hotels", secondary="link_hotel_media", lazy="selectin")

    @hybrid_property
    def sum_rating(self):
        return sum(map(lambda rating_val: rating_val.rating, self.user_ratings)) / len(self.user_ratings) if len(
            self.user_ratings) else 0

    @hybrid_property
    def starting_from(self):
        # Comes room minimum price
        return min(map(lambda room_price: room_price.price, self.available_rooms)) if len(self.available_rooms) else 0

    # @hybrid_property
    # def medias(self):
    #     return [IMediaReadSchema.model_validate(image.media) for image in self.images]

    def __str__(self):
        return self.name


class Freebie(Base):
    name: Mapped[str] = mapped_column()
    logo_url: Mapped[str] = mapped_column(nullable=True)

    # hotels: Mapped[List["Hotel"]] = relationship(back_populates="freebies", secondary="link_freebie_hotel")

    def __str__(self):
        return f"{self.name}"


class Amenity(Base):
    name: Mapped[str] = mapped_column()
    logo_url: Mapped[str] = mapped_column(nullable=True)

    # hotels: Mapped[List["Hotel"]] = relationship(back_populates="amenities", secondary="link_amenity_hotel")

    def __str__(self):
        return f"{self.name}"


class HotelRating(Base):  # M2M
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    comment: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column(nullable=False, default=0)

    hotel_ref: Mapped["Hotel"] = relationship(back_populates="user_ratings", lazy='joined')

    @validates("rating")
    def validate_rating(self, key, rating):
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be in [0,5]")
        return rating

    __table_args__ = (
        CheckConstraint(and_(rating >= 0, rating <= 5)),
        UniqueConstraint("hotel_id", "user_id")
    )


class HotelUserBooking(Base):  # M2M
    id: Mapped[int] = mapped_column(primary_key=False, nullable=True)
    booking_id: Mapped[uuid] = mapped_column(UUID, default=uuid.uuid4, primary_key=True, unique=True)
    available_room_id: Mapped[int] = mapped_column(ForeignKey("available_room.id", ondelete='CASCADE'),
                                                   primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    started_at: Mapped[datetime.date] = mapped_column(Date)
    stopped_at: Mapped[datetime.date] = mapped_column(Date)

    @validates('started_at', 'stopped_at')
    def validate_dates(self, key, field):
        if key == 'stopped_at' and isinstance(self.started_at, datetime):
            if self.started_at > field:
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    "The stopped_at field must be greater-or-equal than the started_at field")
        elif key == 'started_at' and isinstance(self.stopped_at, datetime):
            if self.stopped_at < field:
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    "The stopped_at field must be greater-or-equal than the started_at field")
        return field

    __table_args__ = (
        CheckConstraint(started_at < stopped_at),
    )


class AvailableRoom(Base):
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    price: Mapped[int] = mapped_column(default=0, nullable=False)
    view: Mapped[str] = mapped_column()
    bed: Mapped[int] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    hotel_room: Mapped["Hotel"] = relationship(back_populates='available_rooms', lazy='joined')
    freebies: Mapped[List["Freebie"]] = relationship(secondary=link_freebie_room, lazy="selectin")
    amenities: Mapped[List["Amenity"]] = relationship(secondary=link_amenity_room, lazy="selectin")
    user_room_booking: Mapped[List["User"]] = relationship(secondary='hotel_user_booking', lazy='selectin',
                                                           back_populates='hotel_booking')

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("The price must be positive")
        return price

    __table_args__ = (
        CheckConstraint(price >= 0),
    )