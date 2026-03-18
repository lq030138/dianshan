# 跨境电商资讯每日推荐

## 📰 项目简介

这是专为跨境电商从业者设计的每日行业资讯自动报告系统，每日北京时间 8:00 自动收集整理各大电商平台的最新动态，通过 GitHub Actions 自动发布报告！

## ✅ 核心特性

✨ **自动采集** - 多源新闻自动抓取
🧹 **智能去重** - 同一新闻只保留一条
📊 **自动分类** - 按平台/品类/政策分类
🎨 **精美排版** - 响应式 HTML 页面
☁️ **自动部署** - GitHub Pages 自动发布

## 🚀 快速开始

```bash
git clone <your-repo-url>
cd ai-daily-report
pip install -r requirements.txt
```

## 📅 日报预览

访问 GitHub Pages 分支查看最新日报：
<br/>
- 中文界面：<https://your-username.github.io/ai-daily-report>
<br/>
- English Version: <https://your-username.github.io/ai-daily-report/en/>

## 🔄 每日更新

- **自动触发时间**: 每天北京时间 8:00
- **手动触发**: 通过 `.github/workflows/daily-report.yml` 中的 `workflow_dispatch`
- **延迟处理**: 采集失败不会中断后续任务

## 📚 新闻源列表

- [ ] 阿里巴巴国际站博客
- [X] 亚马逊卖家大学
- [ ] TikTok for Business
- [ ] Temu 卖家中心
- [ ] 速卖通官方博客
- [ ] 跨境电商圈公众号
- [ ] EB 动力网
- [ ] 跨境知道

## 📜 License

MIT License
