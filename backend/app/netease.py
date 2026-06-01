"""网易云客户端封装。

底层是 NeteaseCloudMusicApi（Node 服务）。

要点：
- cookie 通过 POST body 传递（避免 query 编码截断 MUSIC_U 中的 % 字符）
- realIP 伪装大陆出口（海外 VPS 必须）
- song/url 双策略：优先 v1 高音质，回退到老版 br=999000/320000
"""
from __future__ import annotations

import os
import random
from typing import Any, Optional

import httpx

from .config import settings


class NeteaseClient:
    def __init__(self) -> None:
        self.base = settings.NETEASE_API.rstrip("/")
        self.cookie = settings.NETEASE_COOKIE
        self.real_ip = os.getenv("NETEASE_REAL_IP", "116.25.146.177")
        self._client: Optional[httpx.AsyncClient] = None

    async def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=15)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _request(self, path: str, **params: Any) -> dict:
        """统一请求：用 POST + form body，cookie 不走 URL 避免编码丢失。"""
        body: dict[str, Any] = {}
        if self.cookie:
            body["cookie"] = self.cookie
        if self.real_ip:
            body["realIP"] = self.real_ip
        body["timestamp"] = random.randint(10**12, 10**13)
        body.update(params)

        c = await self.client()
        r = await c.post(f"{self.base}{path}", data=body)
        r.raise_for_status()
        return r.json()

    # 兼容旧名
    _get = _request

    async def login_status(self) -> dict:
        return await self._request("/login/status")

    async def search(self, keyword: str, limit: int = 20) -> list[dict]:
        data = await self._request("/cloudsearch", keywords=keyword, limit=limit)
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
        """两条策略尝试拿直链：

        1. /song/url/v1 + level=exhigh→higher→standard（带 VIP 鉴权）
        2. 老接口 /song/url + br=999000→320000→128000（容错更好）

        取到 url 立即返回，并把 http 升级为 https。
        """
        # 策略 A：v1 + level
        for level in ("exhigh", "higher", "standard"):
            url = await self._try_song_url_v1(neid, level)
            if url:
                return url

        # 策略 B：老接口 + br
        for br in (999000, 320000, 128000):
            url = await self._try_song_url_legacy(neid, br)
            if url:
                return url

        return None

    async def _try_song_url_v1(self, neid: int, level: str) -> Optional[str]:
        try:
            data = await self._request("/song/url/v1", id=neid, level=level)
            items = data.get("data") or []
            if items:
                it = items[0]
                url = it.get("url")
                if url:
                    return self._upgrade(url)
                reason = (it.get("freeTrialPrivilege") or {}).get("cannotListenReason")
                print(
                    f"[netease] v1 {neid} level={level} no url: "
                    f"fee={it.get('fee')} code={it.get('code')} reason={reason}"
                )
        except Exception as e:
            print(f"[netease] v1 {neid} level={level} error: {e}")
        return None

    async def _try_song_url_legacy(self, neid: int, br: int) -> Optional[str]:
        try:
            data = await self._request("/song/url", id=neid, br=br)
            items = data.get("data") or []
            if items:
                it = items[0]
                url = it.get("url")
                if url:
                    return self._upgrade(url)
                print(
                    f"[netease] legacy {neid} br={br} no url: "
                    f"fee={it.get('fee')} code={it.get('code')}"
                )
        except Exception as e:
            print(f"[netease] legacy {neid} br={br} error: {e}")
        return None

    @staticmethod
    def _upgrade(url: str) -> str:
        if url.startswith("http://"):
            return "https://" + url[len("http://"):]
        return url

    async def song_meta(self, neid: int) -> Optional[dict]:
        data = await self._request("/song/detail", ids=str(neid))
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
        data = await self._request("/lyric", id=neid)
        return {
            "lrc": (data.get("lrc") or {}).get("lyric", ""),
            "tlyric": (data.get("tlyric") or {}).get("lyric", ""),
        }

    async def playlist_track_ids(self, playlist_id: str) -> list[int]:
        if not playlist_id:
            return []
        data = await self._request("/playlist/track/all", id=playlist_id, limit=200)
        return [s["id"] for s in (data.get("songs") or [])]

    async def search_users(self, keyword: str, limit: int = 12) -> list[dict]:
        """type=1002 搜用户（公开账号）"""
        data = await self._request("/search", keywords=keyword, type=1002, limit=limit)
        users = (data.get("result") or {}).get("userprofiles") or []
        out = []
        for u in users:
            out.append({
                "uid": u.get("userId"),
                "nickname": u.get("nickname", ""),
                "avatar": u.get("avatarUrl", ""),
                "signature": u.get("signature", ""),
            })
        return out

    async def search_playlists(self, keyword: str, limit: int = 20) -> list[dict]:
        """type=1000 搜公开歌单"""
        data = await self._request("/search", keywords=keyword, type=1000, limit=limit)
        items = (data.get("result") or {}).get("playlists") or []
        out = []
        for p in items:
            out.append({
                "id": p.get("id"),
                "name": p.get("name", ""),
                "cover": p.get("coverImgUrl", ""),
                "track_count": p.get("trackCount", 0),
                "play_count": p.get("playCount", 0),
                "creator": (p.get("creator") or {}).get("nickname", ""),
            })
        return out

    async def user_playlists(self, uid: int, limit: int = 50) -> list[dict]:
        """拿一个用户公开的歌单"""
        data = await self._request("/user/playlist", uid=uid, limit=limit)
        items = data.get("playlist") or []
        out = []
        for p in items:
            out.append({
                "id": p.get("id"),
                "name": p.get("name", ""),
                "cover": p.get("coverImgUrl", ""),
                "track_count": p.get("trackCount", 0),
                "play_count": p.get("playCount", 0),
                "creator": (p.get("creator") or {}).get("nickname", ""),
            })
        return out

    async def playlist_tracks(self, playlist_id: int, limit: int = 100) -> list[dict]:
        """歌单里的所有曲目（不是 ID 列表，含元数据）"""
        data = await self._request("/playlist/track/all", id=playlist_id, limit=limit)
        out = []
        for s in (data.get("songs") or []):
            out.append({
                "neid": s["id"],
                "title": s.get("name", ""),
                "artist": ", ".join(a.get("name", "") for a in s.get("ar", [])),
                "album": (s.get("al") or {}).get("name", ""),
                "duration": int((s.get("dt") or 0) / 1000),
                "cover_url": (s.get("al") or {}).get("picUrl", ""),
            })
        return out


netease = NeteaseClient()
