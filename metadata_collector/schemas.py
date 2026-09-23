from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class BaseMetadata(BaseModel):
    """Common envelope fields shared by every metadata schema in the registry."""

    id: str
    timestamp: datetime


class SensorMetadata(BaseMetadata):
    kind: Literal["sensor"] = "sensor"
    device_id: str
    reading: float
    unit: str


class FileMetadata(BaseMetadata):
    kind: Literal["file"] = "file"
    file_name: str
    size_bytes: int
    checksum: str


class TransactionMetadata(BaseMetadata):
    kind: Literal["transaction"] = "transaction"
    account_id: str
    amount: float
    currency: str
