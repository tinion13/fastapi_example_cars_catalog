from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Favorite, User
from exceptions.auth_service_exceptions import AuthError
from utils.user_utils import generate_random_username


class AuthService:
    def __init__(
        self,
        secret_key: str = "CHANGE_ME_SECRET",
        algorithm: str = "HS256",
        access_minutes: int = 60 * 24,
    ) -> None:
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.ACCESS_MIN = access_minutes

        self.pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    async def find_user_by_identifier(
        self,
        session: AsyncSession,
        identifier: str
    ) -> User | None:
        return await session.scalar(select(User).where((User.email.ilike(identifier)) | (User.username.ilike(identifier))))

    async def get_user_by_id(
        self,
        session: AsyncSession,
        uid: int
    ) -> User | None:
        stmt = select(User).options(selectinload(User.favorites).selectinload(Favorite.car)).where(User.id == uid)
        return await session.scalar(stmt)

    async def create_user(
        self,
        session: AsyncSession,
        email: str,
        password: str,
        username: str | None = None
    ) -> tuple[User, None] | tuple[None, str]:
        if await self.find_user_by_identifier(session, email):
            return None, "Пользователь существует!"
        if username and await self.find_user_by_identifier(session, username):
            return None, "Такое имя пользователя существует!"
        if not username:
            while True:
                username = generate_random_username(length=10)
                if not await session.scalar(select(User).where(User.username == username)):
                    break
        user = User(email=email, password_hash=self.pwd.hash(password), username=username, is_admin=False)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user, None

    def make_token(
        self,
        sub: str
    ) -> str:
        exp = datetime.now(UTC) + timedelta(minutes=self.ACCESS_MIN)
        return jwt.encode({"sub": sub, "exp": exp}, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def verify_and_get_user(
        self,
        session: AsyncSession,
        token: str
    ) -> User | None:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        uid = int(payload.get("sub"))
        user = await self.get_user_by_id(session, uid)
        return user

    async def try_get_user(
        self,
        session: AsyncSession,
        token: str | None
    ) -> User | None:
        if not token:
            return None
        try:
            return await self.verify_and_get_user(session, token)
        except AuthError:
            return None
