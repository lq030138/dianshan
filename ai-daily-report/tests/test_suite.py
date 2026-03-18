#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证采集器和日报生成器
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))


def test_rss_fetch():
    """测试 RSS 采集器"""
    from scrapers.rss_feed import RSSFeedScraper
    
    print("🧪 测试 RSSFeedScraper...")
    scraper = RSSFeedScraper({
        'name': '测试新闻源',
        'rss_url': 'http://rss.com/news'  # 替换为实际 RSS 地址
    })
    result = scraper.crawl()
    print(f"  结果：获取 {len(result)} 条新闻")


def test_deduplicate():
    """测试去重功能"""
    from processor.deduplicate import content_deduplicator
    
    print("🧪 测试去重逻辑...")
    test_news = [
        {'title': '测试新闻 1', 'description': '这是第一条测试新闻的内容'},
        {'title': '测试新闻 1', 'description': '这是第一条测试新闻的内容'},  # 重复
        {'title': '测试新闻 2', 'description': '这是第二条测试新闻的内容'}
    ]
    
    result = content_deduplicator.remove_duplicates(test_news)
    print(f"  去重前：{len(test_news)} 条 → 去重后：{len(result)} 条")


def test_classify():
    """测试分类器"""
    from processor.classify import classify_news
    
    print("🧪 测试分类功能...")
    test_news = {
        'title': '阿里巴巴国际站最新政策更新',
        'description': '这是一个关于平台政策的通知'
    }
    
    category = classify_news(test_news)
    print(f"  分类结果：{category}")


def test_generate():
    """测试日报生成器"""
    from generator.create_report import DailyReportGenerator
    
    print("🧪 测试日报生成器...")
    generator = DailyReportGenerator()
    
    test_news = [
        {
            'title': '测试新闻',
            'url': 'https://test.com',
            'description': '这是测试新闻摘要',
            'date': '2026-03-18',
            'category': 'platform'
        }
    ]
    
    # 生成临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        output_path = f.name
    
    generator.render(output_path, test_news)
    print(f"  生成文件：{output_path}")


if __name__ == '__main__':
    print("=" * 50)
    print("🧪 运行测试套件")
    print("=" * 50)
    
    try:
        # 运行各个测试
        test_rss_fetch()
        print("-" * 50)
        test_deduplicate()
        print("-" * 50)
        test_classify()
        print("-" * 50)
        test_generate()
        
        print("=" * 50)
        print("✅ 所有测试通过！")
        
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
