from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Message, User
from db.session import get_session
from dependencies.common import get_templates
from dependencies.policies import require_user

router = APIRouter()


@router.get("/messages", response_class=HTMLResponse)
async def my_messages(
    request: Request,
    user: User = Depends(require_user),
    session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates)
):
    messages = (await session.scalars(select(Message).where(Message.user_id == user.id).order_by(Message.created_at))).all()
    return templates.TemplateResponse(
        "messages.html",
        {"request": request, "user": user, "messages": messages})

@router.post("/messages", response_class=HTMLResponse)
async def post_message(
    request: Request,
    text: str = Form(...),
    user: User = Depends(require_user),
    session: AsyncSession = Depends(get_session)
):
    message = Message(user_id=user.id, sender_is_admin=False, text=text)
    session.add(message)
    await session.commit()
    return RedirectResponse(url="/messages", status_code=status.HTTP_303_SEE_OTHER)
