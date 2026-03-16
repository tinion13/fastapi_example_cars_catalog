from typing import Annotated

from fastapi import Query
from pydantic import BeforeValidator

from services.cars_filter.filter import CarsFilter, CarsQueryParams
from services.cars_filter.filter_builder import build_cars_filter

EmptyToNone = BeforeValidator(lambda v: None if v == "" or v == "None" else v)

OptIntQ = Annotated[int | None, EmptyToNone, Query()]
OptFloatQ = Annotated[float | None, EmptyToNone, Query()]
OptStrQ = Annotated[str | None, EmptyToNone, Query()]
OptStrListQ = Annotated[list[str] | None, Query()]


def cars_filters(
    brand: OptStrQ = None,
    model: OptStrQ = None,
    body_type: OptStrListQ = None,
    fuel: OptStrListQ = None,
    transmission: OptStrListQ = None,
    year_min: OptIntQ = None,
    year_max: OptIntQ = None,
    price_min: OptFloatQ = None,
    price_max: OptFloatQ = None,
    mileage_max: OptIntQ = None,
    power_min: OptIntQ = None,
    sort: OptStrQ = None,
    page: Annotated[int, Query(ge=1)] = 1,
) -> CarsFilter:
    params = CarsQueryParams(
        brand=brand,
        model=model,
        body_type=body_type,
        fuel=fuel,
        transmission=transmission,
        year_min=year_min,
        year_max=year_max,
        price_min=price_min,
        price_max=price_max,
        mileage_max=mileage_max,
        power_min=power_min,
        sort=sort,
        page=page,
    )
    return build_cars_filter(params)
