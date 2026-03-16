from fastapi import Depends, HTTPException, status

from db.models import User
from dependencies.auth import get_user_or_none


async def require_user(
    user: User | None = Depends(get_user_or_none),
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user


async def require_admin(
    user: User = Depends(require_user),
) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user
