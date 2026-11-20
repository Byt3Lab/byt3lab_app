from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from .utils import sanitize_model_data
from ..models.models import Byt3labNgrafixModel


class NgrafixRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labNgrafixModel]:
        stmt = select(Byt3labNgrafixModel)
        if published_only:
            stmt = stmt.where(Byt3labNgrafixModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labNgrafixModel.order_num.asc(), Byt3labNgrafixModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, item_id: int) -> Optional[Byt3labNgrafixModel]:
        stmt = select(Byt3labNgrafixModel).where(Byt3labNgrafixModel.id == item_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_discipline(cls, session, discipline: str) -> List[Byt3labNgrafixModel]:
        stmt = (
            select(Byt3labNgrafixModel)
            .where(Byt3labNgrafixModel.discipline == discipline)
            .where(Byt3labNgrafixModel.is_published.is_(True))
            .order_by(Byt3labNgrafixModel.order_num.asc())
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labNgrafixModel:
        item = Byt3labNgrafixModel(**sanitize_model_data(Byt3labNgrafixModel, data))
        session.add(item)
        await session.flush()
        return item

    @classmethod
    async def update(cls, session, item_id: int, data: dict) -> Optional[Byt3labNgrafixModel]:
        stmt = (
            update(Byt3labNgrafixModel)
            .where(Byt3labNgrafixModel.id == item_id)
            .values(**sanitize_model_data(Byt3labNgrafixModel, data))
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, item_id)

    @classmethod
    async def delete(cls, session, item_id: int) -> bool:
        stmt = delete(Byt3labNgrafixModel).where(Byt3labNgrafixModel.id == item_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
