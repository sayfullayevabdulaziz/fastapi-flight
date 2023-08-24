from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.hotel import Freebie
from app.schemas.freebie_schema import AFreebieCreateSchema, AFreebieUpdateSchema


class CRUDFreebie(CRUDBase[Freebie, AFreebieCreateSchema, AFreebieUpdateSchema]):
    pass


freebie = CRUDFreebie(Freebie)
