#!/usr/bin/env bash
# VPS 上一键更新代码并重启服务
# 用法（在 VPS 项目根目录）：bash update.sh
set -e
cd "$(dirname "$0")"

if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  本地有未提交改动："
  git status --short
  echo
  echo "如要丢弃本地改动后再拉，跑：git stash && bash update.sh"
  exit 1
fi

echo "==> git pull"
git pull --rebase

echo "==> rebuild & restart"
docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build

echo
echo "==> done"
docker compose ps
echo
echo "实时日志：docker compose logs -f backend"
