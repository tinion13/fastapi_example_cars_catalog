from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Car, User
from db.session import get_session
from dependencies.common import get_templates
from dependencies.policies import require_admin
from services.car_characteristic_admin import CarCharacteristic

router = APIRouter()


@router.get("/cars/new", response_class=HTMLResponse)
async def admin_new_car_page(
    request: Request,
    admin: User = Depends(require_admin),
    templates: Jinja2Templates = Depends(get_templates)
):
    empty_car = {
        "brand": "",
        "model": "",
        "year": "",
        "price": "",
        "body_type": "",
        "fuel": "",
        "transmission": "",
        "mileage": "",
        "power": "",
    }
    return templates.TemplateResponse(
        "admin/car_form.html",
        {"request": request, "car": empty_car, "mode": "create", "admin": admin}
    )

@router.post("/cars/new")
async def admin_create_car(
    data: CarCharacteristic,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
):
    car = Car(**data.model_dump())
    session.add(car)
    await session.commit()
    return RedirectResponse("/admin/cars", status_code=status.HTTP_302_FOUND)

@router.get("/cars/{car_id}/edit", response_class=HTMLResponse)
async def admin_edit_car_page(
    car_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(require_admin),
    templates: Jinja2Templates = Depends(get_templates)
):
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(404, detail="Car not found")
    return templates.TemplateResponse(
        "admin/car_form.html",
        {"request": request, "car": car, "mode": "edit", "admin": admin}
    )

@router.post("/cars/{car_id}/edit")
async def admin_edit_car(
    car_id: int,
    data: CarCharacteristic,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
):
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(404, detail="Car not found")

    car.brand = data.brand
    car.model = data.model
    car.year = data.year
    car.price = data.price
    car.body_type = data.body_type
    car.fuel = data.fuel
    car.transmission = data.transmission
    car.mileage = data.mileage
    car.power = data.power

    await session.commit()
    return RedirectResponse("/admin/cars", status_code=status.HTTP_302_FOUND)

@router.post("/cars/{car_id}/delete")
async def admin_delete_car(
    car_id: int,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
):
    car = await session.get(Car, car_id)
    if not car:
        raise HTTPException(404, detail="Car not found")

    await session.delete(car)
    await session.commit()
    return RedirectResponse("/admin/cars", status_code=status.HTTP_302_FOUND)
