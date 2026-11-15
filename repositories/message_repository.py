from __future__ import annotations
from typing import List, Optional
from sqlalchemy import select, update, delete, func
from ..models.models import Byt3labMessageModel


class MessageRepository:

    @classmethod
    async def get_all(cls, session, form_type: Optional[str] = None, status: Optional[str] = None) -> List[Byt3labMessageModel]:
        stmt = select(Byt3labMessageModel)
        if form_type:
            stmt = stmt.where(Byt3labMessageModel.form_type == form_type)
        if status:
            stmt = stmt.where(Byt3labMessageModel.status == status)
        stmt = stmt.order_by(Byt3labMessageModel.created_at.desc(), Byt3labMessageModel.id.desc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def get_by_id(cls, session, message_id: int) -> Optional[Byt3labMessageModel]:
        stmt = select(Byt3labMessageModel).where(Byt3labMessageModel.id == message_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def count_unread(cls, session) -> int:
        stmt = select(func.count(Byt3labMessageModel.id)).where(Byt3labMessageModel.status == "new")
        result = await session.execute(stmt)
        return result.scalar() or 0

    @classmethod
    async def create(cls, session, data: dict) -> Byt3labMessageModel:
        msg = Byt3labMessageModel(**data)
        session.add(msg)
        await session.flush()
        return msg

    @classmethod
    async def update_status(cls, session, message_id: int, status: str) -> Optional[Byt3labMessageModel]:
        stmt = (
            update(Byt3labMessageModel)
            .where(Byt3labMessageModel.id == message_id)
            .values(status=status)
        )
        await session.execute(stmt)
        return await cls.get_by_id(session, message_id)

    @classmethod
    async def delete(cls, session, message_id: int) -> bool:
        stmt = delete(Byt3labMessageModel).where(Byt3labMessageModel.id == message_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
