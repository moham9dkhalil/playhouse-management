"""
Sales Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models import Sale, SaleItem, User, CafeteriaProduct
from app.schemas import SaleCreate, SaleResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale_data: SaleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new sale (for cafeteria products)
    """
    try:
        # Validate customer if provided
        if sale_data.customer_id:
            from app.models import Customer
            customer = db.query(Customer).filter(Customer.id == sale_data.customer_id).first()
            if not customer:
                raise ValueError("Customer not found")
        
        # Calculate total
        total_amount = 0
        for item in sale_data.items:
            product = db.query(CafeteriaProduct).filter(CafeteriaProduct.id == item.product_id).first()
            if not product:
                raise ValueError(f"Product {item.product_id} not found")
            total_amount += product.price * item.quantity
        
        db_sale = Sale(
            customer_id=sale_data.customer_id,
            total_amount=total_amount,
            payment_method=sale_data.payment_method,
            created_by=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.add(db_sale)
        db.flush()
        
        # Add items
        for item in sale_data.items:
            sale_item = SaleItem(
                sale_id=db_sale.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=db.query(CafeteriaProduct).filter(CafeteriaProduct.id == item.product_id).first().price
            )
            db.add(sale_item)
        
        db.commit()
        db.refresh(db_sale)
        return db_sale
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[SaleResponse])
async def list_sales(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all sales with pagination
    """
    sales = db.query(Sale).offset(skip).limit(limit).all()
    return sales

@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific sale
    """
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale
