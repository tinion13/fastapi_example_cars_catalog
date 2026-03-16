from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.session import get_session
from dependencies.common import get_service
from services.auth_service import AuthService


async def get_user_or_none(
    service: AuthService = Depends(get_service),
    session: AsyncSession = Depends(get_session),
    access_token: str | None = Cookie(default=None),
) -> User | None:
    if not access_token:
        return None
    return await service.try_get_user(session, access_token)
