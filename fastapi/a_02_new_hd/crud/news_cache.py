from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cache_categories
from models.news import Category


# 获取分类
async def get_categories(db: AsyncSession, skip: int=0, limit: int=100):

    cache_categories = await get_cached_categories()
    if cache_categories:
        return cache_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories =  result.scalars().all()

    if categories:
        c_str = jsonable_encoder(categories)
        await set_cache_categories(c_str)

    return categories
