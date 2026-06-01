from fastapi import APIRouter
from sqlmodel import select

from ..db import session_scope
from ..models import LyricCache
from ..netease import netease

router = APIRouter(prefix="/api/lyric", tags=["lyric"])


@router.get("/{neid}")
async def get_lyric(neid: int):
    # 先查缓存
    with session_scope() as s:
        row = s.get(LyricCache, neid)
        if row:
            return {"lrc": row.lrc, "tlyric": row.tlyric, "cached": True}

    # 拉网易云
    try:
        data = await netease.lyric(neid)
    except Exception as e:
        return {"lrc": "", "tlyric": "", "error": f"{type(e).__name__}: {e}"}

    lrc = data.get("lrc") or ""
    tly = data.get("tlyric") or ""

    # 写缓存
    with session_scope() as s:
        s.add(LyricCache(neid=neid, lrc=lrc, tlyric=tly))

    return {"lrc": lrc, "tlyric": tly, "cached": False}
