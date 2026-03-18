#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨境电商资讯分类器
自动根据内容识别新闻属于哪个类别
"""

import os
import re

# 定义分类规则
CATEGORIES = {
    'platform': {
        'keywords': ['平台', '政策', '更新', '亚马逊', '淘宝，Temu，TikTok', '独立站'],
        'name': '平台动态'
    },
    'supply_chain': {
        'keywords': ['物流', '供应链', '海运', '空运', '海外仓', '清关', '关税'],
        'name': '供应链'
    },
    'policy': {
        'keywords': ['关税', '合规', '欧盟', 'FDA', 'CE', 'EPR', '政策', '法规'],
        'name': '政策法规'
    },
    'product': {
        'keywords': ['选品', '热销', '新品', '爆款', '销量', '排名', '类目', '增长'],
        'name': '热门品类'
    },
    'finance': {
        'keywords': ['支付', '汇率', '金融', '银行', '资金', '退税', '税务'],
        'name': '支付金融'
    },
    'tech': {
        'keywords': ['AI', '工具', 'SaaS', '软件', '技术', '系统', '自动化'],
        'name': '技术应用'
    },
    'operation': {
        'keywords': ['运营', '推广', '营销', 'SEO', 'SEM', '广告投放', '转化率'],
        'name': '运营干货'
    }
}


def classify_news(news):
    """分类新闻内容
    
    Args:
        news: 新闻数据字典
        
    Returns:
        str: 分类名称（如：平台动态、供应链、政策法规等）
    """
    title = news.get('title