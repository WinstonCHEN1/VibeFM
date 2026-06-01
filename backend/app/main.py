import json
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .auth import user_from_token
from .db import init_db
from .netease import netease
from .radio import radio
from .routers import auth as auth_router
from .routers import queue as queue_router
from .routers import search as search_router
from .ws import hub


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    await radio.start()
    yield
    await radio.stop()
    await netease.close()


app = FastAPI(title="Vibe FM · by cg", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(search_router.router)
app.include_router(queue_router.router)


@app.get("/api/health")
async def health():
    return {"ok": True}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket, token: str = Query(default="")):
    user = user_from_token(token)
    if user is None:
        await ws.close(code=4401)
        return
    await hub.connect(ws, user.nickname)
    try:
        snap = await radio.state_snapshot()
        await ws.send_text(json.dumps({"type": "state", "data": snap}, ensure_ascii=False))
        await hub.broadcast_online()
        while True:
            msg = await ws.receive_text()
            try:
                data = json.loads(msg)
            except Exception:
                continue
            if data.get("type") == "chat":
                content = (data.get("content") or "").strip()
                if content:
                    await hub.broadcast("chat", {"nick": user.nickname, "content": content[:200]})
            elif data.get("type") == "ping":
                await ws.send_text(json.dumps({"type": "pong", "t": data.get("t")}))
    except WebSocketDisconnect:
        pass
    finally:
        await hub.disconnect(ws)
        await hub.broadcast_online()
