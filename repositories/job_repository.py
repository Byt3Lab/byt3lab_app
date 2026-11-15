from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from ..models.models import Byt3labJobModel


class JobRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labJobModel]:
        stmt = select(Byt3labJobModel)
        if published_only:
            stmt = stmt.where(Byt3labJobModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labJobModel.id.desc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, job_id: int) -> Optional[Byt3labJobModel]:
        stmt = select(Byt3labJobModel).where(Byt3labJobModel.id == job_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labJobModel]:
        stmt = select(Byt3labJobModel).where(Byt3labJobModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labJobModel:
        job = Byt3labJobModel(**data)
        session.add(job)
        await session.flush()
        return job

    @classmethod
    async def update(cls, session, job_id: int, data: dict) -> Optional[Byt3labJobModel]:
        stmt = (
            update(Byt3labJobModel)
            .where(Byt3labJobModel.id == job_id)
            .values(**data)
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, job_id)

    @classmethod
    async def delete(cls, session, job_id: int) -> bool:
        stmt = delete(Byt3labJobModel).where(Byt3labJobModel.id == job_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
