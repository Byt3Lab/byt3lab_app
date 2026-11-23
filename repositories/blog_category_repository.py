from __future__ import annotations
from typing import List, Optional, Dict
from sqlalchemy import select, update, delete, func
from .utils import sanitize_model_data
from ..models.models import Byt3labBlogCategoryModel, Byt3labPostModel


class BlogCategoryRepository:

    @classmethod
    async def get_all(cls, session, active_only: bool = True) -> List[Byt3labBlogCategoryModel]:
        stmt = select(Byt3labBlogCategoryModel)
        if active_only:
            stmt = stmt.where(Byt3labBlogCategoryModel.is_active.is_(True))
        stmt = stmt.order_by(Byt3labBlogCategoryModel.order_num.asc(), Byt3labBlogCategoryModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_with_counts(cls, session, lang: str = "fr") -> List[dict]:
        cats = await cls.get_all(session, active_only=True)
        stmt = (
            select(Byt3labPostModel.category_id, func.count(Byt3labPostModel.id))
            .where(Byt3labPostModel.is_published.is_(True))
            .group_by(Byt3labPostModel.category_id)
        )
        res = await session.execute(stmt)
        counts: Dict[Optional[int], int] = {row[0]: row[1] for row in res.all()}
        out = []
        for cat in cats:
            d = cat.to_dict(lang=lang)
            d["posts_count"] = counts.get(cat.id, 0)
            out.append(d)
        return out

    @classmethod
    async def get_by_id(cls, session, category_id: int) -> Optional[Byt3labBlogCategoryModel]:
        stmt = select(Byt3labBlogCategoryModel).where(Byt3labBlogCategoryModel.id == category_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labBlogCategoryModel]:
        stmt = select(Byt3labBlogCategoryModel).where(Byt3labBlogCategoryModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labBlogCategoryModel:
        cat = Byt3labBlogCategoryModel(**sanitize_model_data(Byt3labBlogCategoryModel, data))
        session.add(cat)
        await session.flush()
        return cat

    @classmethod
    async def update(cls, session, category_id: int, data: dict) -> Optional[Byt3labBlogCategoryModel]:
        stmt = (
            update(Byt3labBlogCategoryModel)
            .where(Byt3labBlogCategoryModel.id == category_id)
            .values(**sanitize_model_data(Byt3labBlogCategoryModel, data))
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, category_id)

    @classmethod
    async def delete(cls, session, category_id: int) -> bool:
        stmt = delete(Byt3labBlogCategoryModel).where(Byt3labBlogCategoryModel.id == category_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
