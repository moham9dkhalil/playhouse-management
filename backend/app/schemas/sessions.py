"""
Play Session Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PlaySessionCreate(BaseModel):
    device_id: int
    customer_id: Optional[int] = None
    hourly_rate: Optional[float] = 50.0

class PlaySessionUpdate(BaseModel):
    hourly_rate: Optional[float] = None

class PlaySessionEndRequest(BaseModel):
    extra_cost: Optional[float] = 0
    notes: Optional[str] = None

class PlaySessionResponse(BaseModel):
    id: int
    device_id: int
    customer_id: Optional[int]
    started_at: datetime
    ended_at: Optional[datetime]
    status: str
    hourly_rate: float
    total_cost: Optional[Decimal]
    notes: Optional[str]

    class Config:
        from_attributes = True
