"""电台核心调度。

状态：current_song / started_at
队列：Redis List，元素为 JSON {neid, requester_id, requester_nick, ...}
切歌：APScheduler 在 started_at + duration 触发；同时也接受手动 skip。
"""
from __future__ import annotations

import asyncio
import json
import random
import time
from datetime import datetime, timedelta
from typing import Any, Optional

import redis.asyncio as aioredis
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import settings
from .netease import netease
from .ws import hub

QUEUE_KEY = "fm:queue"
RECENT_KEY = "fm:recent"
STATE_KEY = "fm:state"
CHAT_KEY = "fm:chat"
CHAT_HISTORY_LIMIT = 50
WALL_LIMIT = 20


class Radio:
    def __init__(self) -> None:
        self.redis: Optional[aioredis.Redis] = None
        self.scheduler = AsyncIOScheduler()
        self.current: Optional[dict] = None
        self._fallback_pool: list[int] = []
        self._switch_lock = asyncio.Lock()
        self.frozen: bool = False
        self._frozen_remaining: float = 0.0   # 冻结时记录还剩多少秒

    async def start(self) -> None:
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        self.scheduler.start()
        if settings.FALLBACK_PLAYLIST_ID:
            try:
                self._fallback_pool = await netease.playlist_track_ids(settings.FALLBACK_PLAYLIST_ID)
                print(f"[radio] fallback pool loaded: {len(self._fallback_pool)} tracks")
            except Exception as e:
                print("[radio] fallback playlist preload failed:", e)
        # 启动时先尝试从 redis 恢复上次的当前曲目，避免重启后 current 为空
        try:
            raw = await self.redis.get(STATE_KEY)
            if raw:
                self.current = json.loads(raw)
        except Exception as e:
            print("[radio] restore current from redis failed:", e)

        # 韧性兜底：无论是否有人在线，只要没有当前曲目（含 url 失效）就先抽一首垫着，
        # 防止"重启 + 唯一用户刷新去重导致 thaw 不触发"造成的卡死空播。
        has_playable = bool(self.current and self.current.get("url"))
        if not has_playable:
            try:
                await self.play_next(reason="boot")
            except Exception as e:
                print("[radio] boot play_next failed:", e)

        # 启动时若没人在线则冻结（current 已就绪，等有人来 thaw 续播即可）
        if hub.online_count() == 0:
            await self.freeze()
            print("[radio] no listeners, frozen at boot")

    async def stop(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
        if self.redis:
            await self.redis.close()

    async def enqueue(self, neid: int, requester_id: int, requester_nick: str) -> tuple[bool, str]:
        try:
            return await self._enqueue_inner(neid, requester_id, requester_nick)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False, f"点歌失败：{type(e).__name__}: {e}"

    async def _enqueue_inner(self, neid: int, requester_id: int, requester_nick: str) -> tuple[bool, str]:
        assert self.redis is not None
        if await self.redis.sismember(RECENT_KEY, str(neid)):
            return False, "这首歌还在冷却中，过会儿再点"
        items = await self.redis.lrange(QUEUE_KEY, 0, -1)
        my = sum(1 for raw in items if json.loads(raw).get("requester_id") == requester_id)
        if my >= settings.PER_USER_QUEUE_LIMIT:
            return False, f"你最多同时排 {settings.PER_USER_QUEUE_LIMIT} 首"
        for raw in items:
            if json.loads(raw).get("neid") == neid:
                return False, "队列里已经有这首"

        meta = await netease.song_meta(neid)
        if not meta:
            return False, "找不到这首歌"

        # 预检直链：拿不到就别让它进队列，否则切到它的时候只能默默 skip
        test_url = await netease.song_url(neid)
        if not test_url:
            return False, "这首歌当前不可播放（版权 / 地区 / 试听限制），换一首吧"

        item = {
            "neid": neid,
            "title": meta["title"],
            "artist": meta["artist"],
            "duration": meta["duration"],
            "cover_url": meta["cover_url"],
            "requester_id": requester_id,
            "requester_nick": requester_nick,
        }
        await self.redis.rpush(QUEUE_KEY, json.dumps(item, ensure_ascii=False))
        await self.broadcast_queue()
        return True, "已加入队列"

    async def queue_list(self) -> list[dict]:
        assert self.redis is not None
        items = await self.redis.lrange(QUEUE_KEY, 0, -1)
        return [json.loads(x) for x in items]

    async def pop_queue(self) -> Optional[dict]:
        assert self.redis is not None
        raw = await self.redis.lpop(QUEUE_KEY)
        return json.loads(raw) if raw else None

    async def play_next(self, reason: str = "auto") -> None:
        async with self._switch_lock:
            item = await self.pop_queue()
            if item is None:
                item = await self._pick_fallback()
            if item is None:
                self.current = None
                await hub.broadcast("song_change", None)
                return

            url = await netease.song_url(item["neid"])
            if not url:
                print(f"[radio] resolve failed for {item['neid']}, skipping")
                asyncio.create_task(self.play_next(reason="resolve-fail"))
                return

            now_ms = int(time.time() * 1000)
            duration = max(item.get("duration") or 0, 30)
            self.current = {**item, "url": url, "started_at": now_ms}

            assert self.redis is not None
            await self.redis.set(STATE_KEY, json.dumps(self.current, ensure_ascii=False))
            await self.redis.sadd(RECENT_KEY, str(item["neid"]))
            await self.redis.expire(RECENT_KEY, settings.SAME_SONG_COOLDOWN_SEC)

            self._schedule_next(duration)
            await hub.broadcast("song_change", self._public_state())
            print(f"[radio] now playing: {item['title']} - {item['artist']} ({reason})")

    def _schedule_next(self, duration_sec: int) -> None:
        for job in list(self.scheduler.get_jobs()):
            if job.id == "song_end":
                job.remove()
        run_at = datetime.now() + timedelta(seconds=duration_sec + 1)
        self.scheduler.add_job(
            self._on_song_end,
            "date",
            id="song_end",
            run_date=run_at,
            misfire_grace_time=10,
            replace_existing=True,
        )

    async def _on_song_end(self) -> None:
        await self.play_next(reason="end")

    async def skip(self) -> None:
        await self.play_next(reason="skip")

    async def _pick_fallback(self) -> Optional[dict]:
        if not self._fallback_pool:
            return None
        for _ in range(8):
            neid = random.choice(self._fallback_pool)
            assert self.redis is not None
            if await self.redis.sismember(RECENT_KEY, str(neid)):
                continue
            meta = await netease.song_meta(neid)
            if not meta:
                continue
            return {**meta, "requester_id": None, "requester_nick": "电台"}
        return None

    def _public_state(self) -> Optional[dict]:
        if not self.current:
            return None
        return {
            "neid": self.current["neid"],
            "title": self.current["title"],
            "artist": self.current["artist"],
            "duration": self.current["duration"],
            "cover_url": self.current["cover_url"],
            "url": self.current["url"],
            "started_at": self.current["started_at"],
            "requester_nick": self.current.get("requester_nick"),
        }

    async def state_snapshot(self) -> dict[str, Any]:
        return {
            "current": self._public_state(),
            "queue": await self.queue_list(),
            "online": hub.online_count(),
            "online_list": hub.online_list(),
            "presence": hub.presence_map(),
            "chat_history": await self.chat_history(),
            "frozen": self.frozen,
            "server_time": int(time.time() * 1000),
        }

    async def freeze(self) -> None:
        """没人听了：取消切歌定时器，记录剩余时间。"""
        if self.frozen:
            return
        for job in list(self.scheduler.get_jobs()):
            if job.id == "song_end":
                # 算剩余秒
                if self.current:
                    elapsed = (time.time() * 1000 - self.current["started_at"]) / 1000
                    self._frozen_remaining = max(0, self.current["duration"] - elapsed)
                job.remove()
        self.frozen = True
        print(f"[radio] frozen, {self._frozen_remaining:.1f}s remaining of current track")

    async def thaw(self) -> None:
        """有人来了：解冻并继续播。"""
        if not self.frozen:
            return
        self.frozen = False
        if self.current and self._frozen_remaining > 0:
            # 把 started_at 重设成"现在 - 已播秒数"，相当于把暂停的时间补偿掉
            elapsed = self.current["duration"] - self._frozen_remaining
            new_started = int(time.time() * 1000) - int(elapsed * 1000)
            self.current["started_at"] = new_started
            assert self.redis is not None
            await self.redis.set(STATE_KEY, json.dumps(self.current, ensure_ascii=False))
            self._schedule_next(self._frozen_remaining)
            await hub.broadcast("song_change", self._public_state())
            print(f"[radio] thawed, resume current; +{self._frozen_remaining:.1f}s")
            self._frozen_remaining = 0
        else:
            await self.play_next(reason="thaw")

    async def broadcast_queue(self) -> None:
        await hub.broadcast("queue_update", await self.queue_list())

    async def push_chat(self, nick: str, content: str) -> dict:
        """写入聊天历史，返回带 ts 的消息体。"""
        assert self.redis is not None
        msg = {"nick": nick, "content": content, "ts": int(time.time() * 1000)}
        await self.redis.rpush(CHAT_KEY, json.dumps(msg, ensure_ascii=False))
        await self.redis.ltrim(CHAT_KEY, -CHAT_HISTORY_LIMIT, -1)
        return msg

    async def chat_history(self, limit: int = 20) -> list[dict]:
        if not self.redis:
            return []
        items = await self.redis.lrange(CHAT_KEY, -limit, -1)
        return [json.loads(x) for x in items]

    # ---------- 工位留言板 ----------
    def _wall_key(self, target: str) -> str:
        return f"fm:wall:{target}"

    async def push_wall(self, target: str, nick: str, content: str) -> dict:
        """给某个工位主人留言。"""
        assert self.redis is not None
        msg = {
            "target": target,
            "nick": nick,
            "content": content,
            "ts": int(time.time() * 1000),
        }
        key = self._wall_key(target)
        await self.redis.rpush(key, json.dumps(msg, ensure_ascii=False))
        await self.redis.ltrim(key, -WALL_LIMIT, -1)
        return msg

    async def wall_messages(self, target: str, limit: int = WALL_LIMIT) -> list[dict]:
        if not self.redis:
            return []
        items = await self.redis.lrange(self._wall_key(target), -limit, -1)
        return [json.loads(x) for x in items]


radio = Radio()
