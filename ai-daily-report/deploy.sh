#!/bin/bash
# 部署脚本：将日报提交到 GitHub

set -e

REPO_USER="${USER:-}"
REPO_NAME="${REPO:-}"

echo "🚀 跨境电商日报自动部署..."

# 设置 GitHub 仓库路径（假设是当前项目的 GitHub 关联仓库）
REPO_PATH="$1"

if [ -z "$REPO_PATH" ]; then
    # 使用当前目录关联的 GitHub 仓库
    REPO_PATH="."
    
    # 检查是否已连接 GitHub
    if [ -z "${GITHUB_TOKEN:-}" ]; then
        echo "⚠️  未设置 Github API 令牌，使用默认分支推送..."
    else
        echo "🔑 使用 API 令牌认证..."
    fi
fi

# 获取当前日期
DATE=$(date +%Y-%m-%d)
BRANCH="deploy"

# 创建部署分支（如果不存在）
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

# 添加新日报
git add "reports/daily_${DATE}.html" 2>/dev/null || git add "reports/daily_$DATE/"

# 提交更改
git commit -m "📰 生成日报 $DATE"

# 推送到 GitHub
git push -u origin "$BRANCH"

echo "✅ 日报已部署到 GitHub Pages!"

# 查看发布页面
echo ""
echo "📊 查看日报：http://your-user.github.io/ai-daily-report/daily_${DATE}/"
