from datetime import datetime, timedelta

from fastapi import APIRouter

from ..db import session_scope
from ..models import LyricCache
from ..netease import netease

router = APIRouter(prefix="/api/lyric", tags=["lyric"])

# 空结果只缓存 1 小时（防风控偶发），有内容永久缓存
EMPTY_TTL = timedelta(hours=1)


@router.get("/{neid}")
async def get_lyric(neid: int):
    # 查缓存
    with session_scope() as s:
        row = s.get(LyricCache, neid)
        if row:
            is_empty = not row.lrc
            stale = is_empty and (datetime.utcnow() - row.cached_at > EMPTY_TTL)
            if not stale:
                return {"lrc": row.lrc, "tlyric": row.tlyric, "cached": True}
            # 空缓存过期 → 重新拉
            s.delete(row)

    # 拉网易云
    try:
        data = await netease.lyric(neid)
    except Exception as e:
        # 失败不缓存，让前端重试
        return {"lrc": "", "tlyric": "", "error": f"{type(e).__name__}: {e}"}

    lrc = data.get("lrc") or ""
    tly = data.get("tlyric") or ""

    # 写缓存
    with session_scope() as s:
        # 防并发重复 insert：先查再写
        existing = s.get(LyricCache, neid)
        if existing:
            existing.lrc = lrc
            existing.tlyric = tly
            existing.cached_at = datetime.utcnow()
        else:
            s.add(LyricCache(neid=neid, lrc=lrc, tlyric=tly))

    return {"lrc": lrc, "tlyric": tly, "cached": False}
