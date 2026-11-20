from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from .utils import sanitize_model_data
from ..models.models import Byt3labPostModel


class PostRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labPostModel]:
        stmt = select(Byt3labPostModel)
        if published_only:
            stmt = stmt.where(Byt3labPostModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labPostModel.published_at.desc(), Byt3labPostModel.id.desc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

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
        return post

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
