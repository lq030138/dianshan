#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨境电商资讯采集器
自动从 RSS/API/网页抓取最新资讯
"""

import os
import sys
from pathlib import Path
from feedparser import parse feed
import yaml

# 设置项目路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger, logger


class DailyCrawler:
    """每日日报采集器"""
    
    def __init__(self, config_path='.github/config/sources.yaml'):
        """初始化采集器
        
        Args:
            config_path: 新闻源配置文件路径
        """
        self.config = None
        self.sources = []
        
        # 加载配置
        self._load_config(config_path)
        
        # 初始化采集器实例列表
        self.collectors = []
        
        logger.info(f"✅ 配置已加载，共 {len(self.sources)} 个新闻源")
    
    def _load_config(self, config_path):
        """加载新闻源配置
        
        Args:
            config_path: 配置文件路径
        """
        config_file = PROJECT_ROOT / config_path
        
        self.config = yaml.safe_load(config_file.read_text(encoding='utf-8'))
        self.sources = self.config.get('news_sources', [])
        
        # 从配置创建采集器实例
        for source in self.sources:
            scraper = self._create_scraper(source)
            if scraper:
                self.collectors.append(scraper)
        
        logger.info(f"✅ 已初始化 {len(self.collectors)} 个采集器实例")
        return self.sources
    
    def _create_scraper(self, source):
        """根据配置创建采集器
        
        Args:
            source: 新闻源配置字典
            
        Returns:
            BaseScraper 或 None
        """
        name = source.get('name', 'Unknown')
        
        # 根据来源名称匹配对应的采集器
        if 'aliexpress' in name.lower() or '阿里' in name:
            from scrapers.ali_international import AliScraper
            return AliScraper(source)
        elif 'amazon' in name.lower():
            from scrapers.amazon import AmazonScraper
            return AmazonScraper(source)
        elif 'tiktok' in name.lower():
            from scrapers.tiktok import TikTokScraper
            return TikTokScraper(source)
        elif 'temu' in name.lower():
            from scrapers.temu import TemuScraper
            return TemuScraper(source)
        elif 'shopify' in name.lower():
            from scrapers.shopify import ShopifyScraper
            return ShopifyScraper(source)
        elif 'e-commerce' in name.lower() or 'eb 动力' in name:
            # 通用 RSS 采集器
            from scrapers.rss_feed import RSSFeedScraper
            return RSSFeedScraper(source)
        else:
            # 默认使用 RSS 采集器
            logger.warning(f"⚠️ 未找到对应的采集器，使用RSS模式：{name}")
            from scrapers.rss_feed import RSSFeedScraper
            return RSSFeedScraper(source)
    
    def crawl(self, report_date=None):
        """执行采集任务
        
        Args:
            report_date: 报告日期，格式 YYYY-MM-DD（默认使用今天日期）
            
        Returns:
            list: 采集到的新闻列表
        """
        from processor.deduplicate import content_deduplicator