from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.consts import CARS_PER_PAGE
from db.models import Car, Favorite, User
from db.session import get_session
from dependencies.auth import get_user_or_none
from dependencies.common import get_templates
from dependencies.filter import cars_filters
from dependencies.policies import require_user
from services.cars_filter.filter import CarsFilter
from utils.cars_utils import _sort_table

router = APIRouter()


@router.get("/cars", response_class=HTMLResponse)
async def cars_page(
    request: Request,
    session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates),
    filters: CarsFilter = Depends(cars_filters),
    user: User | None = Depends(get_user_or_none),
):
    stmt = select(Car)
    if filters.conditions:
        stmt = stmt.where(and_(*filters.conditions))

    total_count = await session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    pages = (total_count + CARS_PER_PAGE - 1) // CARS_PER_PAGE if total_count else 1

    order_by = _sort_table(filters.sort)
    if order_by is not None:
        stmt = stmt.order_by(order_by)

    offset = (filters.page - 1) * CARS_PER_PAGE
    cars = (await session.scalars(stmt.offset(offset).limit(CARS_PER_PAGE))).all()

    fav_ids = {fav.car_id for fav in user.favorites} if user else set()

    return templates.TemplateResponse("cars.html", {
        "request": request,
        "cars": cars,
        "sort": filters.sort,
        "fav_ids": fav_ids,
        "page": filters.page,
        "pages": pages,
        "user": user
    })

@router.post("/cars/{car_id}/favorite")
async def toggle_favorite(
    car_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Car not found")
    fav = await session.scalar(select(Favorite).where(Favorite.user_id == user.id,Favorite.car_id == car_id,))
    if fav:
        await session.delete(fav)
        await session.commit()
        return {"favorite": False}
    session.add(Favorite(user_id=user.id, car_id=car_id))
    await session.commit()
    return {"favorite": True}
