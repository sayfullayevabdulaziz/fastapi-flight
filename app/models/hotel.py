import datetime
from typing import List

from sqlalchemy.orm import Mapped, validates
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey
from app.models.base import Base


class Hotel(Base):
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    short_description: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column()
    location: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_recommend: Mapped[bool] = mapped_column(default=True)

    user_ratings: Mapped[List["HotelRating"]] = relationship(back_populates="hotel")
    freebies: Mapped[List["Freebie"]] = relationship(back_populates="hotel_freebie")
    amenities: Mapped[List["Amenity"]] = relationship(back_populates="hotel_amenities")
    available_rooms: Mapped[List["AvailableRoom"]] = relationship(back_populates="hotel_rooms")
    images: Mapped[List["HotelMedia"]] = relationship(back_populates="hotel_image")

    # @hybrid_property
    # def sum_rating(self):
    #     return self.ratings.


class HotelMedia(Base):  # M2M
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)

    media: Mapped["Media"] = relationship(back_populates="hotel_media")


class Freebie(Base):
    name: Mapped[str] = mapped_column()

    def __str__(self):
        return f"{self.name}"


class Amenity(Base):
    name: Mapped[str] = mapped_column()

    def __str__(self):
        return f"{self.name}"


class HotelRating(Base):  # M2M
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    comment: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column(nullable=False, default=0)

    @validates("rating")
    def validate_email(self, key, rating):
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be in [0,5]")
        return rating


class HotelUserBooking(Base):  # M2M
    available_room_id: Mapped[int] = mapped_column(ForeignKey("available_room.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    started_at: Mapped[datetime.datetime] = mapped_column()
    stopped_at: Mapped[datetime.datetime] = mapped_column()

    @validates('started_at', 'stopped_at')
    def validate_dates(self, key, field):
        if key == 'stopped_at' and isinstance(self.started_at, datetime.datetime):
            if self.started_at > field:
                raise AssertionError("The stopped_at field must be greater-or-equal than the started_at field")
        elif key == 'started_at' and isinstance(self.stopped_at, datetime.datetime):
            if self.stopped_at < field:
                raise AssertionError("The stopped_at field must be greater-or-equal than the started_at field")
        return field


class AvailableRoom(Base):
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    price: Mapped[int] = mapped_column(default=0, nullable=False)
    view: Mapped[str] = mapped_column()
    bed: Mapped[str] = mapped_column()

    @validates("price")
    def validate_email(self, key, price):
        if price < 0:
            raise ValueError("The price must be positive")
        return price


class LinkFreebieHotel(Base):  # M2M
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), primary_key=True)
    freebie_id: Mapped[int] = mapped_column(ForeignKey("freebie.id"), primary_key=True)


class LinkAmenityHotel(Base):  # M2M
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), primary_key=True)
    amenity_id: Mapped[int] = mapped_column(ForeignKey("amenity.id"), primary_key=True)
