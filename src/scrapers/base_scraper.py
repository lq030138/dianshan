#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨境电商资讯采集器 - 基础框架
所有采集器继承自此基类
"""

import logging
from abc import ABC, abstractmethod


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """采集器基类，所有具体采集器继承此类"""
    
    def __init__(self, name='', priority=0):
        """初始化采集器
        
        Args:
            name: 新闻源名称
            priority: 优先级（数字越大越优先）
        """
        self.name = name
        self.priority = priority
        self.logger = logging.getLogger(f"scraper.{name}")
    
    @abstractmethod
    def crawl(self):
        """采集新闻方法
        
        Returns:
            list: 新闻列表，每项包含 title, url, description, date, category 等
        """
        pass
    
    def log_result(self, news_list):
        """记录采集结果
        
        Args:
            news_list: 新闻列表
        """
        if not news_list:
            self.logger.info(f"❌ 采集结果：未获取到新闻")
        else:
            self.logger.info(f"✅ 采集成功：{self.name} - 共 {len(news_list)} 条新闻")
            for i, news in enumerate(news_list, 1):
                self.logger.info(f"  - [{i}] {news.get('title', 'N/A')[:50]}...")
                # self.logger.info(f"    URL: {news.get('url', 'N/A')}")
    
    def get_info(self):
        """获取采集器信息
        
        Returns:
            dict: 采集器配置信息
        """
        return {
            'name': self.name,
            'priority': self.priority
        }
    
    def validate(self):
        """验证采集器配置
        
        Returns:
            bool: 验证是否通过
        """
        if not self.name:
            logger.warning(f"❌ 新闻源未设置命名：{self.name}")
            return False
        
        if self.priority < 0:
            logger.warning(f"⚠️  优先级错误（必须>=0）：{self.name} - {self.priority}")
            return True
        
        return True
