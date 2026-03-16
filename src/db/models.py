from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user", cascade="all, delete-orphan", lazy="raise")
    messages: Mapped[list["Message"]] = relationship(back_populates="user", cascade="all, delete-orphan",
                                                     order_by="Message.created_at", lazy="raise")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender_is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="messages")

    __table_args__ = (Index("ix_messages_user_created_at", "user_id", "created_at"),)


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(index=True)
    model: Mapped[str] = mapped_column(index=True)
    year: Mapped[int] = mapped_column(index=True)
    price: Mapped[int] = mapped_column(index=True)
    body_type: Mapped[str] = mapped_column(index=True)
    mileage: Mapped[int] = mapped_column(index=True)
    power: Mapped[int] = mapped_column(index=True)
    fuel: Mapped[str] = mapped_column(index=True)
    transmission: Mapped[str] = mapped_column(index=True)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="car", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("length(trim(brand)) >= 1", name="ck_cars_brand_len"),
        CheckConstraint("length(trim(model)) >= 1", name="ck_cars_model_len"),
        CheckConstraint("year >= 1886", name="ck_cars_year_ge_1886"),
        CheckConstraint("price >= 0", name="ck_cars_price_ge_0"),
        CheckConstraint("length(trim(body_type)) >= 1", name="ck_cars_body_type_len"),
        CheckConstraint("mileage >= 0", name="ck_cars_mileage_ge_0"),
        CheckConstraint("power >= 0", name="ck_cars_power_ge_0"),
        CheckConstraint("length(trim(fuel)) >= 1", name="ck_cars_fuel_len"),
        CheckConstraint("length(trim(transmission)) >= 1", name="ck_cars_transmission_len"),
    )


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"), index=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    car: Mapped["Car"] = relationship(back_populates="favorites")

    __table_args__ = (UniqueConstraint("user_id", "car_id", name="uq_user_car"),)
