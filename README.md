# Vibe FM · by cg

一个朋友圈级的 24h Web 电台，音乐源自网易云（用你的 VIP cookie 解析），登录用户可点歌排队。像素风界面，温暖米色调。

> 仅限私人小圈子使用，请勿公开传播或商用。

## 架构

```
浏览器 ─┬─ HTTP /api/*  ── nginx ── FastAPI ── NeteaseCloudMusicApi
        └─ WebSocket /ws ─┘                    └── Redis (队列/状态)
                                               └── SQLite (用户/历史)
生产环境最外层加 Caddy 接管 80/443，自动 HTTPS。
```

播放同步：服务器维护 `current_song + started_at(ms)`。客户端每次接到 `song_change` 事件就 `audio.currentTime = (Date.now() - started_at)/1000`，所有人对齐。

## 一、本机开发（macOS / Linux）

```bash
cp .env.example .env
# 填 INVITE_CODES、NETEASE_COOKIE、FALLBACK_PLAYLIST_ID

./run.sh    # 一键起服务，自动等待健康
# 浏览器 http://localhost:8080
```

### 拿 VIP cookie

1. 浏览器登录 music.163.com（VIP 账号）
2. F12 → Application → Cookies → 把 `MUSIC_U` 那一段复制出来即可（也可以整段复制）
3. 粘到 `.env` 的 `NETEASE_COOKIE`，重启 backend：`docker compose restart backend`

### 兜底歌单

队列空了会从这里随机抽。歌单 URL 末尾的数字就是 ID，例如 `https://music.163.com/#/playlist?id=2829896389` → `2829896389`。

## 二、AlmaLinux VPS 部署（一键脚本）

不需要备案的海外 VPS，80/443 直接走 Let's Encrypt。

```bash
# 服务器上：
cd /opt
git clone <你的仓库> vibe-fm
cd vibe-fm
sudo bash deploy-almalinux.sh fm.example.com
# 第一次会停下来让你填 .env，填完再跑一次同样命令
```

脚本做的事：装 docker / 开 firewalld 80,443 / 跑 docker compose（含 Caddy 自动 HTTPS）。

### 安全组提醒

云厂商安全组要单独再放 80/443 入站。其他端口（8000、6379、3000）一律不要暴露——只在 docker 网络内通。

## 三、目录结构

```
vibe-fm/
├── docker-compose.yml         # 本地开发（暴露 8080）
├── docker-compose.prod.yml    # 海外 VPS overlay（叠 Caddy + 80/443）
├── .env.example
├── run.sh                     # 本地一键起
├── deploy-almalinux.sh        # AlmaLinux 一键部署
├── caddy/Caddyfile
├── backend/                   # FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py            # 入口 + WebSocket
│       ├── config.py
│       ├── auth.py            # JWT + UserCtx
│       ├── db.py / models.py  # SQLite
│       ├── netease.py         # 网易云客户端
│       ├── radio.py           # 调度核心
│       ├── ws.py              # 广播 hub
│       └── routers/           # auth / search / queue
└── frontend/                  # Vue3 + Vite + Pinia
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── App.vue
        ├── api.js
        ├── utils.js           # 颜色 hash / 头像 / 时间格式
        ├── stores/radio.js    # WebSocket + 状态
        └── components/        # NowPlaying / Queue / SearchPanel /
                               #   ChatPanel / AudiencePanel /
                               #   LoginCard / OnlineList / CatMascot / Avatar
```

## 四、常见问题

- **第一次没声音？** 浏览器自动播放策略会拦首次，页面会出现"CLICK TO PLAY"提示，点一下就好。
- **直链失败 / 403？** VIP cookie 可能过期，更新 `.env` 后 `docker compose restart backend`。
- **想加新邀请码？** 改 `.env` 的 `INVITE_CODES`（逗号分隔），重启 backend。
- **跳过要不要投票？** 当前 MVP 是任何登录用户都能直接 skip。后面要加投票把 `routers/queue.py` 的 `/skip` 改一下即可。
- **国内 VPS 想跑？** 需要域名先备案，或改用非标端口（如 8443）+ Caddy DNS-01 证书。脚本默认按海外环境配置。
