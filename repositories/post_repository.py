from __future__ import annotations
from typing import List, Optional, Tuple
from sqlalchemy import select, update, delete, or_, func
from .utils import sanitize_model_data
from ..models.models import Byt3labPostModel, Byt3labBlogCategoryModel


class PostRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labPostModel]:
        stmt = select(Byt3labPostModel)
        if published_only:
            stmt = stmt.where(Byt3labPostModel.is_published.is_(True))
        stmt = stmt.order_by(
            Byt3labPostModel.is_featured.desc(),
            Byt3labPostModel.published_at.desc(),
            Byt3labPostModel.id.desc(),
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def search_paginated(
        cls,
        session,
        *,
        q: str = "",
        category_slug: str = "",
        tag: str = "",
        page: int = 1,
        per_page: int = 9,
        published_only: bool = True,
    ) -> Tuple[List[Byt3labPostModel], int]:
        stmt = select(Byt3labPostModel)
        count_stmt = select(func.count(Byt3labPostModel.id))

        if published_only:
            stmt = stmt.where(Byt3labPostModel.is_published.is_(True))
            count_stmt = count_stmt.where(Byt3labPostModel.is_published.is_(True))

        if category_slug:
            cat_subq = select(Byt3labBlogCategoryModel.id).where(Byt3labBlogCategoryModel.slug == category_slug)
            stmt = stmt.where(Byt3labPostModel.category_id.in_(cat_subq))
            count_stmt = count_stmt.where(Byt3labPostModel.category_id.in_(cat_subq))

        if tag:
            like_tag = f"%{tag.strip()}%"
            tag_filter = or_(
                Byt3labPostModel.tags_fr.ilike(like_tag),
                Byt3labPostModel.tags_en.ilike(like_tag),
            )
            stmt = stmt.where(tag_filter)
            count_stmt = count_stmt.where(tag_filter)

        if q and q.strip():
            like_q = f"%{q.strip()}%"
            q_filter = or_(
                Byt3labPostModel.title_fr.ilike(like_q),
                Byt3labPostModel.title_en.ilike(like_q),
                Byt3labPostModel.summary_fr.ilike(like_q),
                Byt3labPostModel.summary_en.ilike(like_q),
                Byt3labPostModel.tags_fr.ilike(like_q),
                Byt3labPostModel.tags_en.ilike(like_q),
            )
            stmt = stmt.where(q_filter)
            count_stmt = count_stmt.where(q_filter)

        total = (await session.execute(count_stmt)).scalar() or 0
        page = max(1, page)
        per_page = max(1, min(50, per_page))
        stmt = (
            stmt.order_by(
                Byt3labPostModel.is_featured.desc(),
                Byt3labPostModel.published_at.desc(),
                Byt3labPostModel.id.desc(),
            )
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        rows = list((await session.execute(stmt)).scalars().all())
        return rows, int(total)

    @classmethod
    async def get_related(cls, session, post: Byt3labPostModel, limit: int = 3) -> List[Byt3labPostModel]:
        stmt = select(Byt3labPostModel).where(
            Byt3labPostModel.is_published.is_(True),
            Byt3labPostModel.id != post.id,
        )
        if post.category_id:
            stmt = stmt.order_by(
                (Byt3labPostModel.category_id == post.category_id).desc(),
                Byt3labPostModel.published_at.desc(),
            )
        else:
            stmt = stmt.order_by(Byt3labPostModel.published_at.desc())
        stmt = stmt.limit(limit)
        return list((await session.execute(stmt)).scalars().all())

    @classmethod
    async def increment_views(cls, session, post_id: int) -> None:
        stmt = (
            update(Byt3labPostModel)
            .where(Byt3labPostModel.id == post_id)
            .values(views_count=func.coalesce(Byt3labPostModel.views_count, 0) + 1)
            .execution_options(synchronize_session=False)
        )
        await session.execute(stmt)

    @classmethod
    async def get_by_id(cls, session, post_id: int) -> Optional[Byt3labPostModel]:
        stmt = select(Byt3labPostModel).where(Byt3labPostModel.id == post_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labPostModel]:
        stmt = select(Byt3labPostModel).where(Byt3labPostModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labPostModel:
        post = Byt3labPostModel(**sanitize_model_data(Byt3labPostModel, data))
        session.add(post)
        await session.flush()
        return await cls.get_by_id(session, post.id) or post

    @classmethod
    async def update(cls, session, post_id: int, data: dict) -> Optional[Byt3labPostModel]:
        stmt = (
            update(Byt3labPostModel)
            .where(Byt3labPostModel.id == post_id)
            .values(**sanitize_model_data(Byt3labPostModel, data))
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, post_id)

    @classmethod
    async def delete(cls, session, post_id: int) -> bool:
        stmt = delete(Byt3labPostModel).where(Byt3labPostModel.id == post_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
