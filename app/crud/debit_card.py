from __future__ import annotations

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.debit_card import DebitCard
from app.schemas.debit_schema import ADebitCardCreateSchema, ADebitCardUpdateSchema


class CRUDDebitCard(CRUDBase[DebitCard, ADebitCardCreateSchema, ADebitCardUpdateSchema]):
    async def get_list(self,
                       db_session: AsyncSession,
                       order_by: str = 'created_at',
                       desc: bool = False,
                       where: dict | None = {}
    ):
        columns = self.model.__table__.columns

        query = select(self.model)\
            .options(selectinload(self.model.user_cards))\
            .where(and_(k == v for k, v in where.items()))\
            .order_by(columns[order_by].desc() if desc else columns[order_by].asc())
        # create query
        # execute query
        response = await db_session.execute(query)
        # return response
        return response.scalars().all()


debit_card = CRUDDebitCard(DebitCard)
