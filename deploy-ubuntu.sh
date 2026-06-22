#!/usr/bin/env bash
# Ubuntu (20.04 / 22.04 / 24.04) 一键部署脚本
# 在 root 或带 sudo 的用户下执行：
#   sudo bash deploy-ubuntu.sh [your-domain.com]
#
# 完成的事：
#   1. 装 docker engine + compose plugin（官方 apt 源）
#   2. 开 ufw 80/443（若 ufw 已启用）
#   3. 拉项目（如果没拉，需提供 REPO_URL）
#   4. 用 docker-compose.prod.yml + Caddy 起服务（自动 HTTPS）
set -e

DOMAIN="${1:-}"
PROJECT_DIR="${PROJECT_DIR:-/opt/vibe-fm}"
REPO_URL="${REPO_URL:-}"   # 例如 https://github.com/you/vibe-fm.git

if [ "$EUID" -ne 0 ]; then
  echo "请用 sudo 运行：sudo bash deploy-ubuntu.sh"
  exit 1
fi

# 确认确实是 Ubuntu / Debian 系
if ! command -v apt-get >/dev/null 2>&1; then
  echo "❌ 没找到 apt-get，这个脚本只适用于 Ubuntu/Debian。"
  echo "   AlmaLinux/CentOS 请用 deploy-almalinux.sh"
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

echo "==> [1/5] 装 docker engine + compose plugin"
if ! command -v docker >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y ca-certificates curl gnupg git

  # 添加 Docker 官方 GPG key
  install -m 0755 -d /etc/apt/keyrings
  if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
      | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
  fi

  # 识别发行版代号（Ubuntu 用 ubuntu 源；Debian 系自动回退）
  . /etc/os-release
  REPO_OS="ubuntu"
  if [ "${ID:-ubuntu}" = "debian" ]; then
    REPO_OS="debian"
  fi
  CODENAME="${VERSION_CODENAME:-$(. /etc/os-release && echo "$UBUNTU_CODENAME")}"

  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${REPO_OS} ${CODENAME} stable" \
    > /etc/apt/sources.list.d/docker.list

  apt-get update -y
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker
else
  echo "    docker 已存在，跳过"
  # 确保 git 在
  command -v git >/dev/null 2>&1 || { apt-get update -y && apt-get install -y git; }
fi

echo "==> [2/5] 防火墙开 80/443"
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
  ufw allow 80/tcp
  ufw allow 443/tcp
  ufw reload || true
  echo "    已放行 80/443"
else
  echo "    ufw 未启用，跳过（请确保云厂商安全组放行 80/443）"
fi

echo "==> [3/5] 准备项目目录 $PROJECT_DIR"
if [ ! -d "$PROJECT_DIR" ]; then
  if [ -z "$REPO_URL" ]; then
    echo "    PROJECT_DIR 不存在，且未提供 REPO_URL"
    echo "    请先 git clone 到 $PROJECT_DIR，或："
    echo "    REPO_URL=https://github.com/you/vibe-fm.git sudo bash $0 $DOMAIN"
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
