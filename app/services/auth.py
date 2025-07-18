from datetime import datetime, timedelta, timezone
from typing import ClassVar, Tuple, Optional

from jose import jwt, JWTError
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.auth.config import ALGORITHM, SECRET_KEY, RESET_TOKEN_EXPIRE_MINUTES, RESET_PASSWORD_SECRET_KEY
from app.models.login_request import LoginRequest
from app.models.login_response import LoginResponse
from app.models.user import User
from app.services.users import SqliteUsersService

ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseAuthApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthApi.subclasses += (cls,)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def login_user(self, login_request: LoginRequest, db) -> LoginResponse:
        raise NotImplementedError("login_user must be implemented in a subclass")


class AuthService(BaseAuthApi):
    async def login_user(self, login_request: LoginRequest, db) -> LoginResponse:
        """Authenticate a user with username and password."""
        user: Optional[User] = await SqliteUsersService().get_user_by_name(login_request.username, db)
        if not user or not self.verify_password(login_request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        now = datetime.now(timezone.utc)
        token_data = {
            "sub": user.username,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "iat": int(now.timestamp())
        }

        token = self.create_access_token(token_data)
        return LoginResponse(token=token)

    def create_reset_token(self, email: str) -> str:
        expire = datetime.now() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": email, "exp": expire}
        return jwt.encode(to_encode, RESET_PASSWORD_SECRET_KEY, algorithm=ALGORITHM)

    def verify_reset_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, RESET_PASSWORD_SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=400, detail="Invalid token")
            return email
        except JWTError:
            raise HTTPException(status_code=400, detail="Invalid or expired token")