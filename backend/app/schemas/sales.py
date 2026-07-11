"""
Sales Schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    items: List[SaleItemCreate]
    payment_method: str  # cash, card, loyalty_points

class SaleResponse(BaseModel):
    id: int
    customer_id: Optional[int]
    total_amount: Decimal
    payment_method: str
    created_at: datetime

    class Config:
        from_attributes = True
