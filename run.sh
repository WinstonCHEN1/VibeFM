#!/usr/bin/env bash
# 一键启动 Vibe FM 本地开发环境
# 用法：./run.sh   或   bash run.sh
set -e

cd "$(dirname "$0")"

# ---------- 0. 检查 docker ----------
if ! command -v docker >/dev/null 2>&1; then
  echo "❌ 没找到 docker。请先装 Docker Desktop（或 docker engine），再运行此脚本。"
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo "❌ docker 守护进程没起来。打开 Docker Desktop 应用等它就绪后再跑。"
  exit 1
fi

# ---------- 1. 准备 .env ----------
if [ ! -f .env ]; then
  cp .env.example .env
  echo "✅ 已创建 .env（从 .env.example 复制）"
fi

need_edit=0
grep -q '^NETEASE_COOKIE=$' .env && need_edit=1 || true
grep -q '^FALLBACK_PLAYLIST_ID=$' .env && need_edit=1 || true

if [ "$need_edit" = "1" ]; then
  cat <<EOF

⚠️  .env 里有空字段，建议先填好再起服务（不填也能跑，只是会用默认值）：

   NETEASE_COOKIE=        # 浏览器 music.163.com 登录后 F12 → Cookies 复制 MUSIC_U
   FALLBACK_PLAYLIST_ID=  # 队列空时的兜底歌单 ID（可选）
   INVITE_CODES=          # 邀请码，多个逗号分隔（默认 letmein,radio2026）

按 Enter 继续启动（用当前 .env 配置），或 Ctrl-C 取消去编辑
EOF
  read -r _
fi

# ---------- 2. 起服务 ----------
echo "🚀 docker compose up --build  (首次会拉镜像，可能要 3~5 分钟)"
docker compose up -d --build

# ---------- 3. 等待健康 ----------
PORT=$(grep -E '^HTTP_PORT=' .env | tail -1 | cut -d= -f2)
PORT=${PORT:-8080}

echo -n "⏳ 等待后端就绪 (port=$PORT)"
for i in $(seq 1 60); do
  if curl -fsS "http://localhost:$PORT/api/health" >/dev/null 2>&1; then
    echo " ✅"
    break
  fi
  echo -n "."
  sleep 2
  if [ "$i" = "60" ]; then
    echo
    echo "⚠️  120s 内没起来，看看日志："
    echo "   docker compose logs --tail=80 backend"
    exit 1
  fi
done

cat <<EOF

🎉 跑起来了！

  浏览器打开：   http://localhost:$PORT
  邀请码：       grep INVITE_CODES .env
  实时日志：     docker compose logs -f backend
  停掉：         docker compose down
  重启后端：     docker compose restart backend   # 改完 cookie 之后用

EOF
