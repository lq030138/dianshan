
def content_deduplicator:
    """内容去重器（基于标题+摘要+时间戳）"""
    def remove_duplicates(news_list, threshold=0.8):
        """移除重复新闻
        
        Args:
            news_list: 新闻列表
            threshold: 相似性阈值（默认 0.8）
            
        Returns:
            list: 去重后的新闻列表
        """
        if not news_list:
            return []
        
        from rank_bm25 import BM25Okapi
        from bs4 import BeautifulSoup
        
        # 提取新闻标题和摘要的 token
        tokens_list = []
        for news in news_list:
            title = news.get('title', '')
            desc = news.get('description', '')
            
            # 清理文本
            clean_text = title + desc
            tokens = clean_text.lower().split()
            tokens_list.append(tokens)
        
        # 使用 BM25 算法计算相似性
        bm25 = BM25Okapi(tokens_list)
        scores = [[bm25.get_scores(tokens)] for tokens in tokens_list]
        
        # 基于 score 移除重复项（保留最早的一条）
        keep_indices = []
        for i, news in enumerate(news_list):
            title = news.get('title', '')
            desc = news.get('description', '')
            
            # 检查是否与已保留的新闻重复
            is_duplicate = False
            for j, kept_news in enumerate(keep_indices):
                kept_news = news_list[kept_news]
                kept_title = kept_news.get('title', '')
                kept_desc = kept_news.get('description', '')
                
                # 计算标题相似性
                title_sim = self._similarity(title, kept_title)
                desc_sim = self._similarity(desc, kept_desc)
                
                # 如果相似度过高，认为是重复
                if title_sim > threshold or desc_sim > threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                keep_indices.append(i)
        
        # 返回去重后的新闻
        return [news_list[i] for i in keep_indices]
    
    def _similarity(self, text1, text2):
        """计算文本相似性（简化版）
        
        Args:
            text1: 文本 1
            text2: 文本 2
            
        Returns:
            float: 0-1 之间的相似性分数
        """
        if not text1 or not text2:
            return 0.0
        
        # 简单基于共同词数的相似性
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard 相似性
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        if union == 0:
            return 0.0
        
        return intersection / union
    
