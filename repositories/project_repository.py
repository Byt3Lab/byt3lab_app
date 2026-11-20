from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete
from .utils import sanitize_model_data
from ..models.models import Byt3labProjectModel


class ProjectRepository:

    @classmethod
    async def get_all(cls, session, published_only: bool = True) -> List[Byt3labProjectModel]:
        stmt = select(Byt3labProjectModel)
        if published_only:
            stmt = stmt.where(Byt3labProjectModel.is_published.is_(True))
        stmt = stmt.order_by(Byt3labProjectModel.order_num.asc(), Byt3labProjectModel.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, project_id: int) -> Optional[Byt3labProjectModel]:
        stmt = select(Byt3labProjectModel).where(Byt3labProjectModel.id == project_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_slug(cls, session, slug: str) -> Optional[Byt3labProjectModel]:
        stmt = select(Byt3labProjectModel).where(Byt3labProjectModel.slug == slug)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labProjectModel:
        project = Byt3labProjectModel(**sanitize_model_data(Byt3labProjectModel, data))
        session.add(project)
        await session.flush()
        return project

    @classmethod
    async def update(cls, session, project_id: int, data: dict) -> Optional[Byt3labProjectModel]:
        stmt = (
            update(Byt3labProjectModel)
            .where(Byt3labProjectModel.id == project_id)
            .values(**sanitize_model_data(Byt3labProjectModel, data))
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, project_id)

    @classmethod
    async def delete(cls, session, project_id: int) -> bool:
        stmt = delete(Byt3labProjectModel).where(Byt3labProjectModel.id == project_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
