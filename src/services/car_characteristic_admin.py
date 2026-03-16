from pydantic import BaseModel, Field


class CarCharacteristic(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    body_type: str = Field(min_length=1)
    fuel: str = Field(min_length=1)
    transmission: str = Field(min_length=1)
    year: int = Field(ge=1886)
    price: int = Field(ge=0)
    mileage: int = Field(ge=0)
    power: int = Field(ge=0)
