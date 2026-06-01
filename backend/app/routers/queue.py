from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..auth import current_user
from ..radio import radio

router = APIRouter(prefix="/api", tags=["queue"])


class EnqueueIn(BaseModel):
    neid: int


@router.get("/state")
async def state():
    return await radio.state_snapshot()


@router.post("/queue")
async def enqueue(body: EnqueueIn, user=Depends(current_user)):
    ok, msg = await radio.enqueue(body.neid, user.id, user.nickname)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"ok": True, "msg": msg}


@router.get("/queue")
async def queue():
    return {"items": await radio.queue_list()}


@router.post("/skip")
async def skip(user=Depends(current_user)):
    # MVP：登录用户都能直接 skip。如果需要投票后续再加。
    await radio.skip()
    return {"ok": True}
