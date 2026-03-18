#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用网页采集器 - 适用于不支持 RSS 的网页
"""

import requests
from bs4 import BeautifulSoup
import re


class WebScraper:
    """网页新闻采集器"""
    
    def __init__(self, url, headers=None):
        """初始化采集器
        
        Args:
            url: 目标网址
            headers: HTTP请求头（可选）
        """
        self.url = url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timeout = 30
        self.retry_times = 3
    
    def crawl(self):
        """采集网页新闻
        
        Returns:
            list: 新闻列表
        """
        try:
            for attempt in range(self.retry_times):
                try:
                    response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    return self._extract_news(soup)
                    
                except requests.RequestException as e:
                    print(f"重试次数 {attempt + 1}/{self.retry_times}: {str(e)}")
                    continue
                    
            return []
        
        except Exception as e:
            print(f"❌ 采集失败：{str(e)}")
            return []
    
    def _extract_news(self, soup):
        """从 HTML 中抽取新闻
        
        Args:
            soup: BeautifulSoup 解析对象
            
        Returns:
            list: 新闻列表
        """
        news_list = []
        
        # 尝试常见的新闻容器类名
        article_selectors = [
            "article",
            "div.article",
            "div.post",
            "div.news",
            "div.content",
            ".item",
            ".news-item",
            ".article",
            ".post-item",
            "li.item"
        ]
        
        # 查找所有可能的文章元素
        articles = soup.select(*article_selectors)
        
        # 如果没有找到，尝试查找所有<h2>标题
        if not articles:
            tags = soup.find_all(['h2', 'h3', 'h4'])
            if tags:
                articles = tags
        
        # 遍历文章元素
        for article in articles:
            title = self._extract_title(article)
            link = self._extract_link(article)
            
            # 如果有标题和链接，认为是一篇新闻
            if title and link:
                # 尝试提取摘要
                desc = article.get_text()[:500] if article.get_text().strip() else "未提供摘要"
                
                news_item = {
                    'title': title,
                    'url': link,
                    'description': desc,
                    'source': self.url
                }
                news_list.append(news_item)
        
        return news_list
    
    def _extract_title(self, article):
        """抽取文章标题
        
        Args:
            article: HTML 元素
            
        Returns:
            str: 标题文本
        """
        # 优先查找<h1>、<h2>、<h3>
        title_tags = article.select('*')
        
        for tag in title_tags[:5]:  # 只检查前 5 个标签
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'a']:
                text = tag.get_text(strip=True)
                if text and len(text) > 10:
                    # 排除导航菜单、页脚等常见元素
                    if not any(word in text.lower() for word in ['关于我们', '联系我们', '首页', '登录']):
                        return text
        
        # 如果没有找到合适标题，返回整个文章的第一个文本内容
        text = article.get_text(strip=True)
        if text and len(text) > 20:
            return text[:100]
        
        return None
    
    def _extract_link(self, article):
        """抽取文章链接
        
        Args:
            article: HTML 元素
            
        Returns:
            str: 链接地址
        """
        # 查找链接
        links = article.select('a')
        
        if links:
            # 返回第一个看起来像新闻的链接
            for link in links[:5]:
                href = link.get('href', '')
                
                # 排除内部链接、导航等
                if href.startswith('http') and not any(word in href for word in ['/about', '/contact', '/privacy']
                    )：
                    return href
        
        # 返回当前网页作为备选
        return self.url
    
    def collect_news(self):
        """通用采集接口
        
        返回:
            list: 新闻列表
        """
        return self.crawl()
