from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from ..models.models import Byt3labPartnerModel


class PartnerRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labPartnerModel]:
        stmt = select(Byt3labPartnerModel)
        if published_only:
            stmt = stmt.where(Byt3labPartnerModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labPartnerModel.order_num.asc(), Byt3labPartnerModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, partner_id: int) -> Optional[Byt3labPartnerModel]:
        stmt = select(Byt3labPartnerModel).where(Byt3labPartnerModel.id == partner_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_category(cls, session, category: str) -> List[Byt3labPartnerModel]:
        stmt = (
            select(Byt3labPartnerModel)
            .where(Byt3labPartnerModel.category == category)
            .where(Byt3labPartnerModel.is_published.is_(True))
            .order_by(Byt3labPartnerModel.order_num.asc())
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labPartnerModel:
        partner = Byt3labPartnerModel(**data)
        session.add(partner)
        await session.flush()
        return partner

    @classmethod
    async def update(cls, session, partner_id: int, data: dict) -> Optional[Byt3labPartnerModel]:
        stmt = (
            update(Byt3labPartnerModel)
            .where(Byt3labPartnerModel.id == partner_id)
            .values(**data)
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, partner_id)

    @classmethod
    async def delete(cls, session, partner_id: int) -> bool:
        stmt = delete(Byt3labPartnerModel).where(Byt3labPartnerModel.id == partner_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
