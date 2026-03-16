from typing import Any

from sqlalchemy import asc, desc

from db.models import Car

SORT_MAP = {
        "brand": Car.brand,
        "model": Car.model,
        "year": Car.year,
        "price": Car.price,
        "mileage": Car.mileage,
        "power": Car.power,
        "fuel": Car.fuel,
        "transmission": Car.transmission,
        "body_type": Car.body_type,
    }

def _sort_table(sort: str | None) -> Any:
        if not sort:
            return None
        name, dir_ = sort.split(".", 1)
        col = SORT_MAP.get(name)
        var = desc(col) if dir_.lower() == "desc" else asc(col)
        return var
