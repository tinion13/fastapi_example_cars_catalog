from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.consts import COOKIE_NAME
from db.models import User
from db.session import get_session
from dependencies.auth import get_user_or_none
from dependencies.common import get_service, get_templates
from dependencies.policies import require_user
from services.auth_service import AuthService

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    user: User | None = Depends(get_user_or_none),
):
    if user:
        return RedirectResponse(url="/profile")
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
async def login_action(
    request: Request,
    response: Response,
    identifier: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
    service: AuthService = Depends(get_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    user = await service.find_user_by_identifier(session, identifier)
    if not user or not service.pwd.verify(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Неверный email или имя пользователя или пароль"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    token = service.make_token(str(user.id))
    response = RedirectResponse(url="/cars", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=COOKIE_NAME, value=token,
        httponly=True, samesite="lax", max_age=service.ACCESS_MIN * 60)
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    user: User | None = Depends(get_user_or_none),
):
    if user:
        return RedirectResponse(url="/profile")
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error": None})

@router.post("/register", response_class=HTMLResponse)
async def register_action(
    request: Request,
    response: Response,
    email: str = Form(...),
    username: str | None = Form(None),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
    service: AuthService = Depends(get_service),
    templates: Jinja2Templates = Depends(get_templates)
):
    user, error = await service.create_user(session, email, password, username)
    if error:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": error},
            status_code=status.HTTP_400_BAD_REQUEST)
    if user:
        token = service.make_token(str(user.id))
        response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key=COOKIE_NAME, value=token,
            httponly=True, samesite="lax", max_age=service.ACCESS_MIN * 60)
        return response

@router.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    user: User = Depends(require_user),
    _: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates)
):
    fav_cars = [fav.car for fav in user.favorites]
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user, "fav_cars": fav_cars})

@router.post("/profile", response_class=HTMLResponse)
async def update_username(
    request: Request,
    username: str = Form(...),
    user: User = Depends(require_user),
    session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates)
):
    fav_cars = [fav.car for fav in user.favorites]

    if await session.scalar(select(User).where(User.username == username, User.id != user.id)):
        return templates.TemplateResponse(
            "profile.html",
            {"request": request, "user": user, "fav_cars": fav_cars,
            "error": "Никнейм уже занят", "success": None},
        )
    user.username = username
    await session.commit()
    await session.refresh(user)

    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user, "fav_cars": fav_cars,
        "error": None, "success": "Никнейм успешно изменён"},
    )

@router.post("/logout")
async def logout(
):
    resp = RedirectResponse(url="/cars", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie(COOKIE_NAME)
    return resp


