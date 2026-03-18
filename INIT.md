# 初始化 git 仓库
git init

# 添加所有文件到 .gitignore
git add .

# 创建初始提交
git commit -m "✨ 跨境电商资讯每日报告项目初始提交

✅ 已完成模块:
- 项目框架和文档
- 新闻源配置（15 个源）
- GitHub Actions 工作流
- 采集器框架
- 数据处理模块
- 日报生成器
- 前端模板
- 测试脚本

🎯 核心能力:
- 多源采集（RSS/API/网页）
- 智能去重 (BM25 算法）
- 自动分类 (平台/品类/政策）
- 定时执行 (每日 8 点 UTC+8)
- 自动部署 (GitHub Pages)

📅 访问日报:
  http://your-user.github.io/ai-daily-report
"

# 关联 GitHub 仓库（需要先登录 GitHub 账户）
git remote add origin "https://github.com/YOUR_USERNAME/YOUR_REPO.git"

# 推送到 GitHub
git push -u origin main:main
