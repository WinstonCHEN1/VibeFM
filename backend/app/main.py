import json
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .auth import user_from_token
from .db import init_db
from .netease import netease
from .radio import radio
from .routers import auth as auth_router
from .routers import lyric as lyric_router
from .routers import playlist as playlist_router
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
app.include_router(lyric_router.router)
app.include_router(playlist_router.router)


@app.get("/api/health")
async def health():
    return {"ok": True}


@app.get("/api/diag")
async def diag():
    """自检：看 cookie / VIP / realIP 是否正确。
    无鉴权访问，但只暴露不敏感的字段。"""
    out = {
        "real_ip": netease.real_ip,
        "cookie_set": bool(netease.cookie),
        "cookie_len": len(netease.cookie or ""),
        "login": None,
        "test_song_url": None,
    }
    try:
        ls = await netease.login_status()
        acct = (ls.get("data") or {}).get("account") or {}
        prof = (ls.get("data") or {}).get("profile") or {}
        out["login"] = {
            "logged_in": bool(acct.get("id")),
            "user_id": acct.get("id"),
            "nickname": prof.get("nickname"),
            "vip_type": acct.get("vipType"),
        }
    except Exception as e:
        out["login_error"] = f"{type(e).__name__}: {e}"

    try:
        # 用一个非常通用的 ID 做直链解析测试：周杰伦 - 晴天 (186016)
        test_url = await netease.song_url(186016)
        out["test_song_url"] = bool(test_url)
        if not test_url:
            out["test_song_url_hint"] = "解析失败：cookie/VIP/realIP 有问题，看 docker compose logs backend"
    except Exception as e:
        out["test_song_url_error"] = f"{type(e).__name__}: {e}"
    return out


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket, token: str = Query(default="")):
    user = user_from_token(token)
    if user is None:
        await ws.close(code=4401)
        return
    await hub.connect(ws, user.nickname)
    # 第一个人来 → 解冻
    if hub.online_count() == 1:
        await radio.thaw()
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
                    saved = await radio.push_chat(user.nickname, content[:200])
                    await hub.broadcast("chat", saved)
            elif data.get("type") == "ping":
                await ws.send_text(json.dumps({"type": "pong", "t": data.get("t")}))
            elif data.get("type") == "presence":
                fields: dict = {}
                loc = data.get("location")
                if loc in ("floor", "bar"):
                    fields["location"] = loc
                if "text" in data:
                    fields["text"] = (data.get("text") or "")[:20]
                if "listening" in data:
                    fields["listening"] = bool(data.get("listening"))
                if fields:
                    hub.update_presence(ws, **fields)
                    await hub.broadcast_presence(user.nickname)
            elif data.get("type") == "poke":
                target = (data.get("to") or "").strip()
                emoji = (data.get("emoji") or "👋")[:4]
                if target and target != user.nickname:
                    # 全场广播：所有人都看到 target 工位发光+冒气泡
                    await hub.broadcast(
                        "poke",
                        {"from": user.nickname, "to": target, "emoji": emoji},
                    )
            elif data.get("type") == "wall_post":
                target = (data.get("to") or "").strip()
                content = (data.get("content") or "").strip()
                if target and content:
                    saved = await radio.push_wall(target, user.nickname, content[:140])
                    await hub.broadcast("wall_post", saved)
    except WebSocketDisconnect:
        pass
    finally:
        await hub.disconnect(ws)
        await hub.broadcast_online()
        # 最后一个人走 → 冻结
        if hub.online_count() == 0:
            await radio.freeze()
