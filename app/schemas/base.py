"""
Base schemas for consistent API responses
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, TypeVar, Union

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseMetadata(BaseModel):
    """Base metadata for all responses"""

    requested_at: datetime
    total_groups: int
    applied_filters: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class SalesMetadata(BaseMetadata):
    """Metadata for sales/revenue related responses"""

    currency: str


class BaseResponse(BaseModel, Generic[T]):
    """Generic response envelope for all endpoints"""

    metadata: Union[SalesMetadata, BaseMetadata]
    results: List[T]

    model_config = ConfigDict(from_attributes=True)
