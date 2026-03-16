from dataclasses import dataclass, field

from pydantic import BaseModel, Field
from sqlalchemy.sql.elements import ColumnElement


class CarsQueryParams(BaseModel):
    brand: str | None = None
    model: str | None = None

    body_type: list[str] | None = None
    fuel: list[str] | None = None
    transmission: list[str] | None = None

    year_min: int | None = Field(default=None, ge=1886)
    year_max: int | None = Field(default=None, ge=1886)

    price_min: float | None = Field(default=None, ge=0)
    price_max: float | None = Field(default=None, ge=0)

    mileage_max: int | None = Field(default=None, ge=0)
    power_min: int | None = Field(default=None, ge=0)

    sort: str | None = None
    page: int = Field(default=1, ge=1)


@dataclass(slots=True)
class CarsFilter:
    conditions: list[ColumnElement[bool]] = field(default_factory=list)
    sort: str | None = None
    page: int = 1
