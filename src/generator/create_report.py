#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成日报页面
"""

import os
from datetime import datetime
from jinja2 import Template


class DailyReportGenerator:
    """每日日报生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.template_file = os.path.join(os.path.dirname(__file__), 'templates/report_base.html')

    def render(self, output_path, news_list):
        """生成日报页面
        
        Args:
            output_path: 输出文件路径
            news_list: 新闻列表
        """
        if not news_list:
            # 无新闻时的空页面
            self._render_empty_page(output_path)
            return
        
        # 数据预处理
        data = self._prepare_data(news_list)
        
        # 渲染模板
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.render_html(data))
    
    def _render_empty_page(self, output_path):
        """渲染空页面"""
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template_str = f.read()
        
        # 替换{{date}}为空
        html = template_str.replace('{{date}}', '')
        html = html.replace('{{newsList}}', '')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _prepare_data(self, news_list):
        """准备渲染数据
        
        Args:
            news_list: 新闻列表
            
        Returns:
            dict: 渲染数据
        """
        # 按日期排序（最新的在前）
        sorted_news = sorted(news_list, key=lambda x: x.get('date