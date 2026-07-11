"""
Device Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlaystationDeviceCreate(BaseModel):
    device_name: str
    serial_number: str
    console_type: str  # PS4, PS5, Xbox One, etc.
    location: str

class PlaystationDeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class PlaystationDeviceResponse(BaseModel):
    id: int
    device_name: str
    serial_number: str
    console_type: str
    location: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: int

    class Config:
        from_attributes = True
