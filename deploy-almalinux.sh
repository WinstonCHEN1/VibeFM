#!/usr/bin/env bash
# AlmaLinux 9 一键部署脚本
# 在 root 或带 sudo 的用户下执行：
#   sudo bash deploy-almalinux.sh [your-domain.com]
#
# 完成的事：
#   1. 装 docker / docker compose plugin
#   2. 开 firewalld 80/443
#   3. 拉项目（如果没拉）
#   4. 用 docker-compose.prod.yml + Caddy 起服务
set -e

DOMAIN="${1:-}"
PROJECT_DIR="${PROJECT_DIR:-/opt/vibe-fm}"
REPO_URL="${REPO_URL:-}"   # 例如 git@github.com:you/vibe-fm.git

if [ "$EUID" -ne 0 ]; then
  echo "请用 sudo 运行：sudo bash deploy-almalinux.sh"
  exit 1
fi

echo "==> [1/5] 装 docker + compose plugin"
if ! command -v docker >/dev/null 2>&1; then
  dnf -y install dnf-plugins-core
  dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker
else
  echo "    docker 已存在，跳过"
fi

echo "==> [2/5] 防火墙开 80/443"
if systemctl is-active --quiet firewalld; then
  firewall-cmd --permanent --add-service=http
  firewall-cmd --permanent --add-service=https
  firewall-cmd --reload
fi

echo "==> [3/5] 准备项目目录 $PROJECT_DIR"
if [ ! -d "$PROJECT_DIR" ]; then
  if [ -z "$REPO_URL" ]; then
    echo "    PROJECT_DIR 不存在，且未提供 REPO_URL"
    echo "    请先 git clone 到 $PROJECT_DIR，或："
    echo "    REPO_URL=git@github.com:you/vibe-fm.git sudo bash $0 $DOMAIN"
    exit 1
  fi
  git clone "$REPO_URL" "$PROJECT_DIR"
fi
cd "$PROJECT_DIR"

echo "==> [4/5] 准备 .env"
if [ ! -f .env ]; then
  cp .env.example .env
  echo
  echo "    !! 请编辑 .env 然后重新运行 !!"
  echo "    必填："
  echo "      INVITE_CODES=letmein,你的码"
  echo "      NETEASE_COOKIE=MUSIC_U=xxxxx"
  echo "      FALLBACK_PLAYLIST_ID=2829896389"
  if [ -n "$DOMAIN" ]; then
    echo "      DOMAIN=$DOMAIN  (将自动追加)"
    echo "DOMAIN=$DOMAIN" >> .env
  else
    echo "      DOMAIN=fm.example.com"
  fi
  echo
  echo "    编辑命令： vi $PROJECT_DIR/.env"
  exit 0
fi

if [ -n "$DOMAIN" ] && ! grep -q "^DOMAIN=" .env; then
  echo "DOMAIN=$DOMAIN" >> .env
fi

if ! grep -q "^DOMAIN=" .env; then
  echo "    .env 缺少 DOMAIN，请加 DOMAIN=fm.example.com"
  exit 1
fi

echo "==> [5/5] 起服务（含 Caddy 自动 HTTPS）"
docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env up -d --build

echo
echo "✅ 部署完成"
echo
DOMAIN_VAL=$(grep '^DOMAIN=' .env | cut -d= -f2)
echo "   访问：https://$DOMAIN_VAL"
echo "   日志：cd $PROJECT_DIR && docker compose logs -f backend"
echo "   状态：cd $PROJECT_DIR && docker compose ps"
echo
echo "首次申请 Let's Encrypt 证书需要 30~60 秒，第一次访问可能要等一下"
