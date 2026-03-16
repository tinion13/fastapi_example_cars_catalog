from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from routers.admins.base import router as admin_router
from routers.admins.cars import router as admin_cars_router
from routers.admins.cars_actions import router as admin_cars_actions_router
from routers.admins.users import router as admin_users_router
from routers.cars_router import router as cars_router
from routers.users.auth import router as auth_router
from routers.users.messaging import router as messaging_router

router = APIRouter()
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(admin_cars_router, prefix="/admin", tags=["admin:cars"])
router.include_router(admin_cars_actions_router, prefix="/admin", tags=["admin:cars_actions"])
router.include_router(admin_users_router, prefix="/admin", tags=["admin:users"])
router.include_router(auth_router, tags=["users:auth"])
router.include_router(messaging_router, tags=["users:messaging"])
router.include_router(cars_router, tags=["cars"])


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request
):
    return RedirectResponse(url="/cars", status_code=status.HTTP_302_FOUND)
