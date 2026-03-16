from db.models import Car
from services.cars_filter.filter import CarsFilter, CarsQueryParams


def build_cars_filter(params: CarsQueryParams) -> CarsFilter:
    conds = []

    if params.brand:
        conds.append(Car.brand.ilike(f"%{params.brand}%"))
    if params.model:
        conds.append(Car.model.ilike(f"%{params.model}%"))
    if params.body_type:
        conds.append(Car.body_type.in_(params.body_type))
    if params.fuel:
        conds.append(Car.fuel.in_(params.fuel))
    if params.transmission:
        conds.append(Car.transmission.in_(params.transmission))
    if params.year_min is not None:
        conds.append(Car.year >= params.year_min)
    if params.year_max is not None:
        conds.append(Car.year <= params.year_max)
    if params.price_min is not None:
        conds.append(Car.price >= params.price_min)
    if params.price_max is not None:
        conds.append(Car.price <= params.price_max)
    if params.mileage_max is not None:
        conds.append(Car.mileage <= params.mileage_max)
    if params.power_min is not None:
        conds.append(Car.power >= params.power_min)

    return CarsFilter(
        conditions=conds,
        sort=params.sort,
        page=params.page,
    )
