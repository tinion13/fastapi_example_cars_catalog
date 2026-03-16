from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Message, User
from db.session import get_session
from dependencies.common import get_templates
from dependencies.policies import require_admin

router = APIRouter()


@router.get("/users", response_class=HTMLResponse)
async def list_users(
    request: Request,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(require_admin),
    templates: Jinja2Templates = Depends(get_templates)
):
    users = (await session.scalars(select(User).order_by(User.id))).all()
    return templates.TemplateResponse(
        "admin/users.html",
        {"request": request, "users": users, "admin": admin})

@router.post("/users/{user_id}/toggle", response_class=HTMLResponse)
async def toggle_admin(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(require_admin),
    templates: Jinja2Templates = Depends(get_templates)
):
    _user = await session.get(User, user_id)
    if admin.id == user_id:
        return templates.TemplateResponse(
            "admin/users.html",
            {"request": request, "users": [], "error": "Admin cant switch his role", "admin": admin})
    if not _user:
        return templates.TemplateResponse(
            "admin/users.html",
            {"request": request, "users": [], "error": "User not found", "admin": admin})
    _user.is_admin = not bool(_user.is_admin)
    session.add(_user)
    await session.commit()
    return RedirectResponse(url="/admin/users", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/conversations", response_class=HTMLResponse)
async def admin_conversations(
    request: Request,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(require_admin),
    templates: Jinja2Templates = Depends(get_templates)
):
    users = (await session.scalars(select(User).join(Message).distinct().order_by(User.id))).all()
    conversations = []
    for _user in users:
        last = await session.scalar(select(Message).where(Message.user_id == _user.id).order_by(Message.created_at.desc()).limit(1))
        conversations.append({"_user": _user, "last": last.created_at if last else None})
    return templates.TemplateResponse(
        "admin/conversations.html",
        {"request": request, "conversations": conversations, "admin": admin})

@router.get("/conversations/{user_id}", response_class=HTMLResponse)
async def view_conversation(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(require_admin),
    templates: Jinja2Templates = Depends(get_templates)
):
    _user = await session.get(User, user_id)
    if not _user:
        return templates.TemplateResponse("admin/conversation.html", {"request": request, "error": "User not found", "messages": [], "user": None})
    messages = (await session.scalars(select(Message).where(Message.user_id == user_id).order_by(Message.created_at))).all()
    return templates.TemplateResponse("admin/conversation.html", {"request": request, "messages": messages, "_user": _user, "admin": admin})

@router.post("/conversations/{user_id}/reply", response_class=HTMLResponse)
async def reply_conversation(
    request: Request,
    user_id: int,
    text: str = Form(...),
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin)
):
    _user = session.get(User, user_id)
    if not _user:
        return RedirectResponse(url="/admin/conversations", status_code=status.HTTP_303_SEE_OTHER)
    message = Message(user_id=user_id, sender_is_admin=True, text=text)
    session.add(message)
    await session.commit()
    return RedirectResponse(url=f"/admin/conversations/{user_id}", status_code=status.HTTP_303_SEE_OTHER)
