# 跨境电商资讯每日推荐 - 项目使用指南

## 📦 项目说明

这是一个自动化的跨境电商行业资讯日报生成系统，每日 8:00 自动采集各大电商平台最新资讯，生成 HTML 日报报告并发布到 GitHub Pages！

## ✅ 核心功能

- 📡 **多源采集**: RSS/API/网页抓取三种模式
- 🧹 **智能去重**: 基于标题 + 摘要的内容相似度检测
- 📊 **自动分类**: 按平台/品类/政策自动打标
- 🎨 **精美排版**: 响应式 HTML 页面
- ☁️ **自动部署**: GitHub Actions 定时执行

## 🚀 快速开始

### 1. 克隆代码

```bash
git clone <your-repo-url>
cd ai-daily-report
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行测试

```bash
python tests/test_suite.py
```

### 4. 手动触发日报

```bash
cd src
python collect.py
```

### 5. 查看日报

访问 GitHub Pages 页面查看当日报告：


```http://your-username.github.io/ai-daily-report
```

## 📅 自动执行

项目配置为北京时间 8:00 自动执行，你只需：

1. **提交初始化**:
   ```bash
   git init
   git add .
   git commit -m "初始提交"
   ```

2. **连接 GitHub 仓库**:
   ```bash
   git remote add origin <your-github-url>
   ```

3. **开启 GitHub Pages**:
   - 仓库 Settings → Pages → 选择分支 main → 保存

4. **定时任务已自动配置**:
   GitHub Actions 每日 8:00 自动执行采集并发布！

## 🌐 新闻源配置

编辑`src/config/sources.yaml`:

```yaml
news_sources:
  # 添加新的新闻源
  - name: "你的新闻源名称"
    rss_url: "rss 订阅地址"
    category: "自动分类名"
    priority: 5
```

## 🔧 常用命令

### 手动触发日报

```bash
python src/collect.py
```

### 查看昨日日报

```bash
cat reports/daily_Y-Y-M-D.html
```

### 清除旧日报

```bash
rm reports/daily_*.html
```

## 📊 监控与日志

- 查看采集日志: `logs/collect_YYYYMMDD.log`
- 查看 GitHub Actions 运行记录：
  https://github.com/your-user/rep
  o/actions/runs/

## 🎨 样式定制

编辑`src/templates/report_base.html`修改样式

## 🔮 高级功能

### 自定义采集规则

在`src/config/sources.yaml`中定义：

```yaml
- name: "高级新闻源"
  rss_url: "https://example.com/rss"
  category: "特殊分类"
  keywords: ["关键词 1", "关键词 2"]
  fetch_url: "备选网址"
  priority: 10
```

### 启用 OCR 日志价格监测（可选）

```bash
pip install pytesseract
```

### 禁用某些源

在`sources.yaml`中注释掉：

```yaml
- name: "不需要的源"
  rss_url: ""  # 设为空即禁用
```

## ⚠️ 故障排查

### ❌ 采集失败

1. 检查网络连接
2. 查看日志：`logs/*/`
3. 检查 RSS 链接是否有效
4. 确认目标网站未屏蔽爬虫

### ❓ 日报未生成

1. GitHub Actions 是否在运行？检查：`https://github.com/you/yourepo/actions`
2. 是否有错误日志？查看：`logs/`
3. 确认代码无语法错误
4. 尝试手动执行：`python src/collect.py`

### ❄️ 日报页面无新闻

1. 新闻源本身无内容
2. RSS 配置有误
3. 检查网络是否被墙

## 🚀 进阶建议

### 1. 添加 Telegram 推送

```bash
pip install python-telegram-bot
```

在 GitHub Actions 中添加：

```yaml
- name: 发送 Telegram 通知
  run: |
     python -c "..."
```

### 2. 定时邮件提醒

```yaml
- name: 发送邮件
  run: |
     # 邮件配置
```

### 3. 添加更多新闻源

1. 在`sources.yaml`中添加配置
2. 使用 `RSSFeedScraper` 或自定义采集器
3. 重启

### 4. 优化采集速度

1. 使用代理池（如果网络不稳定）
2. 增加并发采集（使用 asyncio）
3. 缓存常用网页（减少重复请求）

## 📜 License

MIT License

## 👤 维护者

婉秋 - 温柔知性的女秘书型 AI 助手