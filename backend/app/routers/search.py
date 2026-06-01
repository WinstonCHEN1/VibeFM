from fastapi import APIRouter, Depends, Query

from ..auth import current_user
from ..netease import netease

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
async def search(q: str = Query(..., min_length=1), limit: int = 20, _user=Depends(current_user)):
    return {"items": await netease.search(q, limit=limit)}
