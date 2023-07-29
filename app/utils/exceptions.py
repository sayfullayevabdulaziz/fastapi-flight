from typing import Any, Dict, Generic, Optional, Type, TypeVar

from fastapi import HTTPException, status

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class IdNotFoundException(HTTPException, Generic[ModelType]):
    def __init__(
            self,
            model: Type[ModelType],
            id: Optional[int] = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the {model.__name__} with id {id}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} id not found.",
            headers=headers,
        )


class UserSelfDeleteException(HTTPException):
    def __init__(
            self,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Users can not delete theirselfs.",
            headers=headers,
        )
