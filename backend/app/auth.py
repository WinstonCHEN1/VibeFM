from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlmodel import select

from .config import settings
from .db import session_scope
from .models import User as UserDB

ALG = "HS256"
TOKEN_TTL = timedelta(days=30)

bearer = HTTPBearer(auto_error=False)


@dataclass
class UserCtx:
    """轻量、可脱离 session 安全使用的用户上下文。"""
    id: int
    nickname: str


def create_token(user_id: int, nickname: str) -> str:
    payload = {
        "sub": str(user_id),
        "nick": nickname,
        "exp": datetime.utcnow() + TOKEN_TTL,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALG)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALG])
    except JWTError:
        return None


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> UserCtx:
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    data = decode_token(creds.credentials)
    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="bad token")
    with session_scope() as s:
        user = s.exec(select(UserDB).where(UserDB.id == int(data["sub"]))).first()
        if not user:
            raise HTTPException(status_code=401, detail="user not found")
        # 在 session 还活着时把字段读出来，返回脱离 session 的轻量对象
        return UserCtx(id=user.id, nickname=user.nickname)


def user_from_token(token: Optional[str]) -> Optional[UserCtx]:
    if not token:
        return None
    data = decode_token(token)
    if not data:
        return None
    with session_scope() as s:
        user = s.exec(select(UserDB).where(UserDB.id == int(data["sub"]))).first()
        if not user:
            return None
        return UserCtx(id=user.id, nickname=user.nickname)
