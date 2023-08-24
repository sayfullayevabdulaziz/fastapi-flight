import datetime
from typing import List

from sqlalchemy.ext.hybrid import hybrid_property
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

    user_ratings: Mapped[List["HotelRating"]] = relationship(back_populates="hotel_ref", lazy="selectin")
    freebies: Mapped[List["Freebie"]] = relationship(back_populates="hotels",
                                                     secondary="link_freebie_hotel",
                                                     lazy="selectin")
    amenities: Mapped[List["Amenity"]] = relationship(back_populates="hotels",
                                                      secondary="link_amenity_hotel",
                                                      lazy="selectin")
    available_rooms: Mapped[List["AvailableRoom"]] = relationship(lazy="selectin")
    images: Mapped[List["Media"]] = relationship(back_populates="hotels", secondary="hotel_media", lazy="selectin")

    @hybrid_property
    def sum_rating(self):
        return sum(map(lambda rating_val: rating_val.rating, self.user_ratings)) / len(self.user_ratings) if len(
            self.user_ratings) else 0

    # @hybrid_property
    # def medias(self):
    #     return [IMediaReadSchema.model_validate(image.media) for image in self.images]


class HotelMedia(Base):  # M2M
    id: Mapped[int] = mapped_column(nullable=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id", ondelete="CASCADE"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)

    # media: Mapped["Media"] = relationship(backref="hotel_media", lazy="selectin")


class Freebie(Base):
    name: Mapped[str] = mapped_column()

    hotels: Mapped[List["Hotel"]] = relationship(back_populates="freebies", secondary="link_freebie_hotel")

    def __str__(self):
        return f"{self.name}"


class Amenity(Base):
    name: Mapped[str] = mapped_column()

    hotels: Mapped[List["Hotel"]] = relationship(back_populates="amenities", secondary="link_amenity_hotel")

    def __str__(self):
        return f"{self.name}"


class HotelRating(Base):  # M2M
    id: Mapped[int] = mapped_column(nullable=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    comment: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column(nullable=False, default=0)

    hotel_ref: Mapped["Hotel"] = relationship(back_populates="user_ratings")

    @validates("rating")
    def validate_rating(self, key, rating):
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be in [0,5]")
        return rating


class HotelUserBooking(Base):  # M2M
    id: Mapped[int] = mapped_column(nullable=True)
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
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    price: Mapped[int] = mapped_column(default=0, nullable=False)
    view: Mapped[str] = mapped_column()
    bed: Mapped[str] = mapped_column()

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("The price must be positive")
        return price


class LinkFreebieHotel(Base):  # M2M
    id: Mapped[int] = mapped_column(nullable=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id", ondelete='CASCADE'), primary_key=True)
    freebie_id: Mapped[int] = mapped_column(ForeignKey("freebie.id"), primary_key=True)


class LinkAmenityHotel(Base):  # M2M
    id: Mapped[int] = mapped_column(nullable=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id", ondelete="CASCADE"), primary_key=True)
    amenity_id: Mapped[int] = mapped_column(ForeignKey("amenity.id"), primary_key=True)
