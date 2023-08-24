from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.media import Media
from app.schemas.media_schema import IMediaCreateSchema, IMediaUpdateSchema


class CRUDMedia(CRUDBase[Media, IMediaCreateSchema, IMediaUpdateSchema]):
    pass


media = CRUDMedia(Media)
