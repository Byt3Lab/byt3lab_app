from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from .utils import sanitize_model_data
from ..models.models import Byt3labServiceModel


class ServiceRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labServiceModel]:
        stmt = select(Byt3labServiceModel)
        if published_only:
            stmt = stmt.where(Byt3labServiceModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labServiceModel.order_num.asc(), Byt3labServiceModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, service_id: int) -> Optional[Byt3labServiceModel]:
        stmt = select(Byt3labServiceModel).where(Byt3labServiceModel.id == service_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labServiceModel]:
        stmt = select(Byt3labServiceModel).where(Byt3labServiceModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labServiceModel:
        service = Byt3labServiceModel(**sanitize_model_data(Byt3labServiceModel, data))
        session.add(service)
        await session.flush()
        return service

    @classmethod
    async def update(cls, session, service_id: int, data: dict) -> Optional[Byt3labServiceModel]:
        stmt = (
            update(Byt3labServiceModel)
            .where(Byt3labServiceModel.id == service_id)
            .values(**sanitize_model_data(Byt3labServiceModel, data))
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, service_id)

    @classmethod
    async def delete(cls, session, service_id: int) -> bool:
        stmt = delete(Byt3labServiceModel).where(Byt3labServiceModel.id == service_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
