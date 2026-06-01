"""WebSocket 连接管理：广播 + 在线列表。

<20 人场景，单进程内存里维护连接列表就够了。
"""
from __future__ import annotations

import asyncio
import json
from typing import Any

from fastapi import WebSocket


class ConnectionHub:
    def __init__(self) -> None:
        self._conns: dict[WebSocket, str] = {}  # ws -> nickname
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket, nickname: str) -> None:
        await ws.accept()
        async with self._lock:
            self._conns[ws] = nickname

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._conns.pop(ws, None)

    def online_count(self) -> int:
        return len(self._conns)

    def online_list(self) -> list[str]:
        # 去重，保持顺序
        seen = set()
        out = []
        for n in self._conns.values():
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

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

    async def broadcast_online(self) -> None:
        await self.broadcast("online", {"count": self.online_count(), "list": self.online_list()})


hub = ConnectionHub()
