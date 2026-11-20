from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from .utils import sanitize_model_data
from ..models.models import Byt3labDivisionModel


class DivisionRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labDivisionModel]:
        stmt = select(Byt3labDivisionModel)
        if published_only:
            stmt = stmt.where(Byt3labDivisionModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labDivisionModel.order_num.asc(), Byt3labDivisionModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, division_id: int) -> Optional[Byt3labDivisionModel]:
        stmt = select(Byt3labDivisionModel).where(Byt3labDivisionModel.id == division_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labDivisionModel]:
        stmt = select(Byt3labDivisionModel).where(Byt3labDivisionModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labDivisionModel:
        division = Byt3labDivisionModel(**sanitize_model_data(Byt3labDivisionModel, data))
        session.add(division)
        await session.flush()
        return division

    @classmethod
    async def update(cls, session, division_id: int, data: dict) -> Optional[Byt3labDivisionModel]:
        stmt = (
            update(Byt3labDivisionModel)
            .where(Byt3labDivisionModel.id == division_id)
            .values(**sanitize_model_data(Byt3labDivisionModel, data))
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, division_id)

    @classmethod
    async def delete(cls, session, division_id: int) -> bool:
        stmt = delete(Byt3labDivisionModel).where(Byt3labDivisionModel.id == division_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
