#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用 RSS 采集器 - 适用于大多数支持 RSS 的新闻源
"""

import feedparser
import html2text


class RSSFeedScraper:
    """RSS 新闻采集器"""
    
    def __init__(self, source_config):
        """初始化采集器
        
        Args:
            source_config: 新闻源配置字典
        """
        self.name = source_config.get('name', 'Unknown RSS Source')
        self.rss_url = source_config.get('rss_url', '')
        self.fetch_url = source_config.get('fetch_url', '')
        self.categories = source_config.get('category', 'uncategorized')
        self.keywords = source_config.get('keywords', [])
        self.priority = source_config.get('priority', 0)
        
        logger.info(f"✅ 初始化 RSS 采集器：{self.name}")
    
    def crawl(self, timeout=30):
        """采集新闻
        
        Args:
            timeout: 请求超时时间（秒）
            
        Returns:
            list: 新闻列表，每项包含：
                - title: 新闻标题
                - url: 新闻链接
                - description: 摘要
                - date: 发布日期
                - category: 分类
                - source: 来源名称
        """
        try:
            if not self.rss_url:
                return []
            
            # 使用 feedparser 解析 RSS
            try:
                feed = parse(self.rss_url, timeout=timeout)
                
                if not feed.entries:
                    logger.warning(f"⚠️ RSS 无内容：{self.name}")
                    return []
                
                news_list = []
                
                # 遍历RSS条目，收集新闻数据
                for entry_feed in feed.entries:
                    news = {
                        'title': entry_feed.get('title', ''),
                        'url': entry_feed.get('links', [{}]) if hasattr(entry_feed, 'links') else entry_feed.get('link', feed.items),
                        'description': entry_feed.get('description', '') or entry_feed.get('summary', ''),
                        'date': self._parse_date(entry_feed.get('published_parsed', None)),
                        'category': self.categories,
                        'source': self.name
                    }
                    news_list.append(news)
                
                logger.info(f"✅ RSS 采集成功：{self.name} - {len(news_list)}条新闻")
                return news_list
                
            except Exception as e:
                logger.error(f"❌ RSS 解析异常：{self.name} - {str(e)}")
                # 尝试使用 fetch_url 替代
                return self._fallback_crawl()
        
        except Exception as e:
            logger.error(f"❌ RSS 采集失败：{self.name} - {str(e)}")
            return []
    
    def _parse_date(self, parsed_date):
        """解析日期格式
        
        Args:
            parsed_date: 解析后的日期对象
            
        Returns:
            str: 格式化日期（YYYY-MM-DD）
        """
        if not parsed_date:
            return None
        
        try:
            from datetime import datetime
            dt = datetime(*parsed_date[:6])
            return dt.strftime("%Y-%m-%d")
        except:
            return None
    
    def _fallback_crawl(self):
        """备用采集方式（当RSS失败时使用）
        
        Returns:
            list: 新闻列表或空列表
        """
        try:
            from scrapers.base_scraper import WebScraper
            scraper = WebScraper(self.fetch_url)
            return scraper.collect_news()
        
        except Exception as e:
            logger.error(f"❌ 备用采集失败：{self.name} - {str(e)}")
            return []
    
    def get_keywords_summary(self):
        """获取新闻源的关键信息
        
        Returns:
            dict: 新闻源配置信息
        """
        return {
            'name': self.name,
            'url': self.rss_url or self.fetch_url,
            'category': self.categories,
            'keywords': self.keywords
        }
