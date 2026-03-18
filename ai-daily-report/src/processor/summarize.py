#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据摘要生成器
为每条新闻生成简短摘要
"""


def extract_summary(news, max_length=300):
    """提取或生成新闻摘要
    
    Args:
        news: 新闻数据字典
        max_length: 摘要最大字符数（默认 300）
        
    Returns:
        str: 摘要文本
    """
    title = news.get('title', '')
    desc = news.get('description', '')
    
    # 如果有摘要，直接返回（清理格式）
    if desc and len(desc) > 50:
        # 清理换行和多余空格
        cleaned = ' '.join(desc.split())
        # 如果超过最大长度，截断
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length] + '...'
        return cleaned
    
    # 如果只有标题，基于标题生成简短摘要
    if title:
        return f"[关于{title}的报道]"
    
    return ""


def generate_daily_summary(news_list):
    """生成每日日报摘要
    
    Args:
        news_list: 新闻列表
        
    Returns:
        dict: 摘要信息（包含每日摘要、重点新闻等）
    """
    if not news_list:
        return {"summary": "今日暂无新闻", "highlights": []}
    
    # 统计分类
    categories_count = {}
    for news in news_list:
        category = news.get('category', 'unknown')
        categories_count[category] = categories_count.get(category, 0) + 1
    
    # 选取前 3 条重点新闻
    sorted_news = sorted(news_list, key=lambda x: x.get('date', ''), reverse=True)
    highlights = []
    for news in sorted_news[:3]:
        highlights.append({
            "title": news.get('title', ''),
            "url": news.get('url', ''),
            "category": news.get('category