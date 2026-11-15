from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from ..models.models import Byt3labSolutionModel


class SolutionRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labSolutionModel]:
        stmt = select(Byt3labSolutionModel)
        if published_only:
            stmt = stmt.where(Byt3labSolutionModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labSolutionModel.order_num.asc(), Byt3labSolutionModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, solution_id: int) -> Optional[Byt3labSolutionModel]:
        stmt = select(Byt3labSolutionModel).where(Byt3labSolutionModel.id == solution_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labSolutionModel]:
        stmt = select(Byt3labSolutionModel).where(Byt3labSolutionModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_division(cls, session, division_slug: str) -> List[Byt3labSolutionModel]:
        stmt = (
            select(Byt3labSolutionModel)
            .where(Byt3labSolutionModel.division_slug == division_slug)
            .where(Byt3labSolutionModel.is_published.is_(True))
            .order_by(Byt3labSolutionModel.order_num.asc())
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labSolutionModel:
        solution = Byt3labSolutionModel(**data)
        session.add(solution)
        await session.flush()
        return solution

    @classmethod
    async def update(cls, session, solution_id: int, data: dict) -> Optional[Byt3labSolutionModel]:
        stmt = (
            update(Byt3labSolutionModel)
            .where(Byt3labSolutionModel.id == solution_id)
            .values(**data)
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, solution_id)

    @classmethod
    async def delete(cls, session, solution_id: int) -> bool:
        stmt = delete(Byt3labSolutionModel).where(Byt3labSolutionModel.id == solution_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
