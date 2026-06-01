from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import select

from ..auth import create_token
from ..config import invite_code_set
from ..db import session_scope
from ..models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginIn(BaseModel):
    invite_code: str = Field(..., min_length=1, max_length=64)
    nickname: str = Field(..., min_length=1, max_length=24)


class LoginOut(BaseModel):
    token: str
    user_id: int
    nickname: str


@router.post("/login", response_model=LoginOut)
def login(body: LoginIn) -> LoginOut:
    if body.invite_code.strip() not in invite_code_set():
        raise HTTPException(status_code=403, detail="邀请码不对")
    nick = body.nickname.strip()
    with session_scope() as s:
        existing = s.exec(select(User).where(User.nickname == nick)).first()
        if existing:
            user = existing
        else:
            user = User(nickname=nick, invite_code=body.invite_code.strip())
            s.add(user)
            s.flush()
        # 关键：在 session 关闭前把要用的字段读出来，否则 commit 后属性 expire 会再次触发 DetachedInstanceError
        uid = user.id
        unick = user.nickname
        token = create_token(uid, unick)
    return LoginOut(token=token, user_id=uid, nickname=unick)
