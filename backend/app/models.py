from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str = Field(index=True)
    invite_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Song(SQLModel, table=True):
    neid: int = Field(primary_key=True)
    title: str
    artist: str = ""
    album: str = ""
    duration: int = 0
    cover_url: str = ""
    cached_at: datetime = Field(default_factory=datetime.utcnow)


class PlayHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    song_neid: int = Field(index=True)
    requester_id: Optional[int] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    skipped: bool = False


class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    nickname: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LyricCache(SQLModel, table=True):
    neid: int = Field(primary_key=True)
    lrc: str = ""
    tlyric: str = ""
    cached_at: datetime = Field(default_factory=datetime.utcnow)
