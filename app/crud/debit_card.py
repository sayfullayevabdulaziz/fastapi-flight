from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.debit_card import DebitCard
from app.schemas.debit_schema import ADebitCardCreateSchema, ADebitCardUpdateSchema


class CRUDDebitCard(CRUDBase[DebitCard, ADebitCardCreateSchema, ADebitCardUpdateSchema]):
    pass


debit_card = CRUDDebitCard(DebitCard)
