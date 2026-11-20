from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from .utils import sanitize_model_data
from ..models.models import Byt3labTeamModel


class TeamRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labTeamModel]:
        stmt = select(Byt3labTeamModel)
        if published_only:
            stmt = stmt.where(Byt3labTeamModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labTeamModel.order_num.asc(), Byt3labTeamModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, member_id: int) -> Optional[Byt3labTeamModel]:
        stmt = select(Byt3labTeamModel).where(Byt3labTeamModel.id == member_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labTeamModel]:
        stmt = select(Byt3labTeamModel).where(Byt3labTeamModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labTeamModel:
        member = Byt3labTeamModel(**sanitize_model_data(Byt3labTeamModel, data))
        session.add(member)
        await session.flush()
        return member

    @classmethod
    async def update(cls, session, member_id: int, data: dict) -> Optional[Byt3labTeamModel]:
        stmt = (
            update(Byt3labTeamModel)
            .where(Byt3labTeamModel.id == member_id)
            .values(**sanitize_model_data(Byt3labTeamModel, data))
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, member_id)

    @classmethod
    async def delete(cls, session, member_id: int) -> bool:
        stmt = delete(Byt3labTeamModel).where(Byt3labTeamModel.id == member_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
