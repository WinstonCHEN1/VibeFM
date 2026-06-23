#!/usr/bin/env bash
# VPS 上一键更新代码并重启服务
# 用法（在 VPS 项目根目录）：sudo bash update.sh
set -e
cd "$(dirname "$0")"

# 选择 overlay：优先用本机的 docker-compose.local.yml（含 REAL_IP、127.0.0.1 端口绑定等本机定制）
# 没有 local.yml 时才回退到 prod.yml（海外 VPS + Caddy 方案）
if [ -f docker-compose.local.yml ]; then
  OVERLAY="docker-compose.local.yml"
else
  OVERLAY="docker-compose.prod.yml"
fi
echo "==> 使用 overlay: $OVERLAY"

if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  本地有未提交改动："
  git status --short
  echo
  echo "如要丢弃本地改动后再拉，跑：git stash && sudo bash update.sh"
  exit 1
fi

echo "==> git pull"
git pull --rebase

echo "==> rebuild & restart"
docker compose -f docker-compose.yml -f "$OVERLAY" --env-file .env up -d --build

echo
echo "==> done"
docker compose -f docker-compose.yml -f "$OVERLAY" ps
echo
echo "实时日志：docker compose logs -f backend"
