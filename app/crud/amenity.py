from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.hotel import Amenity
from app.schemas.amenity_schema import AAmenityCreateSchema, AAmenityUpdateSchema


class CRUDAmenity(CRUDBase[Amenity, AAmenityCreateSchema, AAmenityUpdateSchema]):
    pass


amenity = CRUDAmenity(Amenity)
