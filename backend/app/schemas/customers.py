"""
Customer Schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    email: Optional[str]
    date_of_birth: Optional[date]
    address: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
