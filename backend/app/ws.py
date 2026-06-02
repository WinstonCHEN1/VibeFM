"""WebSocket 连接管理：广播 + 在线列表 + presence。

<20 人场景，单进程内存里维护连接列表就够了。

presence 数据结构（v2）：
{
  nickname: {
    location: "floor" | "bar",
    text:     "摸鱼中" | ...,        # 用户自填，<= 20 字
    last_seen: 1717000000,           # 心跳/动作时间
  }
}
一个用户可能开多个标签页，按 nickname 合并；location 取"最后一次更新"的那个。
"""
from __future__ import annotations

import asyncio
import json
import time
from typing import Any

from fastapi import WebSocket


class ConnectionHub:
    def __init__(self) -> None:
        self._conns: dict[WebSocket, str] = {}  # ws -> nickname
        # 每个 ws 自己的 presence；下线就清掉
        self._ws_presence: dict[WebSocket, dict] = {}
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket, nickname: str) -> None:
        await ws.accept()
        async with self._lock:
            self._conns[ws] = nickname
            self._ws_presence[ws] = {
                "location": "floor",
                "text": "",
                "listening": False,
                "last_seen": int(time.time()),
            }

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._conns.pop(ws, None)
            self._ws_presence.pop(ws, None)

    def online_count(self) -> int:
        return len(set(self._conns.values()))

    def online_list(self) -> list[str]:
        # 去重，保持顺序
        seen: set[str] = set()
        out: list[str] = []
        for n in self._conns.values():
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

    def presence_map(self) -> dict[str, dict]:
        """按 nickname 合并：同一个用户多个标签页时，取最近更新的那个。"""
        merged: dict[str, dict] = {}
        for ws, nick in self._conns.items():
            p = self._ws_presence.get(ws)
            if not p:
                continue
            cur = merged.get(nick)
            if cur is None or p["last_seen"] >= cur["last_seen"]:
                merged[nick] = dict(p)
        return merged

    def update_presence(self, ws: WebSocket, **fields) -> dict | None:
        """更新某个连接的 presence；返回合并后该 nickname 的最新 presence（用于广播）。"""
        if ws not in self._ws_presence:
            return None
        p = self._ws_presence[ws]
        for k, v in fields.items():
            if k in ("location", "text", "listening"):
                p[k] = v
        p["last_seen"] = int(time.time())
        nick = self._conns.get(ws)
        if not nick:
            return None
        return self.presence_map().get(nick)

    def find_ws_by_nick(self, nickname: str) -> list[WebSocket]:
        return [ws for ws, n in self._conns.items() if n == nickname]

    async def broadcast(self, event: str, data: Any) -> None:
        payload = json.dumps({"type": event, "data": data}, ensure_ascii=False)
        async with self._lock:
            dead: list[WebSocket] = []
            for ws in self._conns:
                try:
                    await ws.send_text(payload)
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self._conns.pop(ws, None)
                self._ws_presence.pop(ws, None)

    async def send_to(self, nickname: str, event: str, data: Any) -> None:
        """给指定 nickname 的所有连接发一条消息（戳一下用）。"""
        payload = json.dumps({"type": event, "data": data}, ensure_ascii=False)
        targets = self.find_ws_by_nick(nickname)
        for ws in targets:
            try:
                await ws.send_text(payload)
            except Exception:
                pass

    async def broadcast_online(self) -> None:
        await self.broadcast(
            "online",
            {
                "count": self.online_count(),
                "list": self.online_list(),
                "presence": self.presence_map(),
            },
        )

    async def broadcast_presence(self, nickname: str) -> None:
        """单人状态变更的轻量广播。"""
        p = self.presence_map().get(nickname)
        if p is None:
            return
        await self.broadcast("presence", {"nick": nickname, **p})


hub = ConnectionHub()
