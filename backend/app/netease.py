"""网易云客户端封装。

底层是 NeteaseCloudMusicApi（Node 服务）。
我们在每个请求里挂上用户 cookie，以拿到 VIP 直链。
"""
from __future__ import annotations

import random
from typing import Any, Optional

import httpx

from .config import settings


class NeteaseClient:
    def __init__(self) -> None:
        self.base = settings.NETEASE_API.rstrip("/")
        self.cookie = settings.NETEASE_COOKIE
        self._client: Optional[httpx.AsyncClient] = None

    async def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=15)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

        async def _get(self, path: str, **params: Any) -> dict:
        if self.cookie:
            params.setdefault("cookie", self.cookie)
        # 海外 IP 风控：伪装成大陆 IP 调网易云
        params.setdefault("realIP", "116.25.146.177")
        params.setdefault("timestamp", random.randint(10**12, 10**13))
        c = await self.client()
        r = await c.get(f"{self.base}{path}", params=params)
        r.raise_for_status()
        return r.json()


    async def search(self, keyword: str, limit: int = 20) -> list[dict]:
        data = await self._get("/cloudsearch", keywords=keyword, limit=limit)
        songs = (data.get("result") or {}).get("songs") or []
        out = []
        for s in songs:
            out.append({
                "neid": s["id"],
                "title": s.get("name", ""),
                "artist": ", ".join(a.get("name", "") for a in s.get("ar", [])),
                "album": (s.get("al") or {}).get("name", ""),
                "duration": int((s.get("dt") or 0) / 1000),
                "cover_url": (s.get("al") or {}).get("picUrl", ""),
            })
        return out

        async def song_url(self, neid: int) -> Optional[str]:
        for level in ("exhigh", "higher", "standard"):
            try:
                data = await self._get("/song/url/v1", id=neid, level=level)
                items = data.get("data") or []
                if items:
                    it = items[0]
                    url = it.get("url")
                    if url:
                        if url.startswith("http://"):
                            url = "https://" + url[len("http://"):]
                        return url
                    print(f"[netease] {neid} level={level} no url: fee={it.get('fee')} code={it.get('code')}")
            except Exception as e:
                print(f"[netease] {neid} level={level} error: {e}")
        return None


    async def song_meta(self, neid: int) -> Optional[dict]:
        data = await self._get("/song/detail", ids=str(neid))
        songs = data.get("songs") or []
        if not songs:
            return None
        s = songs[0]
        return {
            "neid": s["id"],
            "title": s.get("name", ""),
            "artist": ", ".join(a.get("name", "") for a in s.get("ar", [])),
            "album": (s.get("al") or {}).get("name", ""),
            "duration": int((s.get("dt") or 0) / 1000),
            "cover_url": (s.get("al") or {}).get("picUrl", ""),
        }

    async def lyric(self, neid: int) -> dict:
        data = await self._get("/lyric", id=neid)
        return {
            "lrc": (data.get("lrc") or {}).get("lyric", ""),
            "tlyric": (data.get("tlyric") or {}).get("lyric", ""),
        }

    async def playlist_track_ids(self, playlist_id: str) -> list[int]:
        if not playlist_id:
            return []
        data = await self._get("/playlist/track/all", id=playlist_id, limit=200)
        return [s["id"] for s in (data.get("songs") or [])]


netease = NeteaseClient()
