from fastapi import APIRouter, Depends, HTTPException, Query

from ..auth import current_user
from ..netease import netease

router = APIRouter(prefix="/api/playlist", tags=["playlist"])


@router.get("/search-users")
async def search_users(q: str = Query(..., min_length=1), _user=Depends(current_user)):
    return {"items": await netease.search_users(q)}


@router.get("/search")
async def search_playlists(q: str = Query(..., min_length=1), _user=Depends(current_user)):
    return {"items": await netease.search_playlists(q)}


@router.get("/by-user/{uid}")
async def user_playlists(uid: int, _user=Depends(current_user)):
    return {"items": await netease.user_playlists(uid)}


@router.get("/{pid}/tracks")
async def playlist_tracks(pid: int, _user=Depends(current_user)):
    items = await netease.playlist_tracks(pid)
    if not items:
        raise HTTPException(status_code=404, detail="歌单为空或无权访问（可能是私密歌单）")
    return {"items": items}
