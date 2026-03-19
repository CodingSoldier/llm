# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value
from typing import List, Dict, Any, Optional

from config.cache_config import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"


# 获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)


# 写入新闻分类缓存: 缓存的数据, 过期时间
# 分类、配置 7200；列表： 600； 详情： 1800；验证码：120 -- 数据越稳定，缓存越持久
# 避免所有key同时过期 引起缓存雪崩
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)

