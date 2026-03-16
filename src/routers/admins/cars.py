from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.consts import CARS_PER_PAGE
from db.models import Car, User
from db.session import get_session
from dependencies.common import get_templates
from dependencies.filter import cars_filters
from dependencies.policies import require_admin
from services.cars_filter.filter import CarsFilter
from utils.cars_utils import _sort_table

router = APIRouter()


@router.get("/cars", response_class=HTMLResponse)
async def cars_page(
    request: Request,
    session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates),
    filters: CarsFilter = Depends(cars_filters),
    admin: User = Depends(require_admin),
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

    return templates.TemplateResponse("admin/cars_list.html", {
        "request": request,
        "cars": cars,
        "sort": filters.sort,
        "page": filters.page,
        "pages": pages,
        "admin": admin
    })
