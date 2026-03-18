#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨境电商资讯采集器 - 主入口脚本
每天 8:00 自动执行采集并生成日报
"""

import sys
import os
import logging
from pathlib import Path
from datetime import datetime
from scrape import DailyCrawler
from processor.deduplicate import content_deduplicator
from processor.classify import classify_news
from processor.summarize import extract_summary, generate_daily_summary
from generator.create_report import DailyReportGenerator

# 配置日志
PROJECT_ROOT = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


def setup_logging():
    """配置日志系统"""
    # 创建 logs 目录
    log_dir = PROJECT_ROOT / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # 日志文件配置
    log_file = log_dir / f'collect_{datetime.now().strftime("%Y%m%d")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def run_daily_report():
    """执行每日日报生成任务"""
    logger.info("🚀 跨境电商日报采集任务开始")
    logger.info("=" * 60)
    
    try:
        # 1. 初始化采集器
        config_path = PROJECT_ROOT / 'src' / 'config' / 'sources.yaml'
        crawler = DailyCrawler(str(config_path))
        
        logger.info(f"✅ 加载新闻源配置：{len(crawler.sources)} 个源")
        logger.info("=" * 60)
        
        # 2. 执行采集
        logger.info("📡 开始采集新闻...")
        news_list = crawler.crawl()
        
        if not news_list:
            logger.warning("⚠️  未采集到任何新闻，任务结束")
            return
        
        logger.info(f"✅ 采集成功，共获取 {len(news_list)} 条新闻")
        logger.info("=" * 60)
        
        # 3. 去重处理
        deduplicated = content_deduplicator.remove_duplicates(news_list)
        logger.info(f"🧹 去重前：{len(news_list)} 条 → 去重后：{len(deduplicated)} 条")
        
        logger.info("=" * 60)
        
        # 4. 分类处理
        with_classification = []
        for news in deduplicated:
            category = classify_news(news)
            news['category'] = category
            with_classification.append(news)
        
        logger.info("✅ 自动分类完成")
        
        # 5. 生成日报
        report_dir = PROJECT_ROOT / 'reports'
        report_dir.mkdir(exist_ok=True)
        
        # 生成文件名
        report_date = datetime.now().strftime('%Y-%m-%d')
        report_path = report_dir / f'daily_{report_date}.html'
        
        # 创建日报生成器
        generator = DailyReportGenerator()
        generator.render(report_path, with_classification)
        
        logger.info(f"✅ 日报生成完成：{report_path}")
        logger.info("=" * 60)
        
        # 6. 提交到 GitHub
        import subprocess
        try:
            subprocess.run(['git', 'add', str(report_path)], 
                          check=True, capture_output=True, text=True)
            subprocess.run(['git', 'commit', '-m', f"📰 生成日报 daily_{report_date}"],
                          check=True, capture_output=True, text=True)
            subprocess.run(['git', 'push', 'origin', 'main'],
                          check=True, capture_output=True, text=True)
            
            logger.info("✅ 提交到 GitHub 成功")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ GitHub 提交失败：{e}")
        except Exception as e:
            logger.error(f"❌ GitHub 提交异常：{str(e)}")
        
        # 7. 输出总结统计
        category_count = {}
        for news in with_classification:
            category = news.get('category', 'unknown')
            category_count[category] = category_count.get(category, 0) + 1
        
        logger.info("📊 日报总结统计：")
        logger.info("-" * 40)
        for category, count in category_count.items():
            logger.info(f"  {category}: {count} 条")
        
        logger.info("=" * 60)
        logger.info("🎉 任务执行完成")
        
        return with_classification
        
    except Exception as e:
        logger.error(f"❌ 任务执行失败：{str(e)}")
        raise
    
    finally:
        logger.info("=" * 60)
        logger.info("📋 任务结束")


if __name__ == '__main__':
    logger.info("📦 跨境电商日报生成器 v1.0")
    run_daily_report()
