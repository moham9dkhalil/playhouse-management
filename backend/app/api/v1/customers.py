"""
Customers Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import Customer, User
from app.schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)
from app.services.customer_service import CustomerService
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new customer
    """
    service = CustomerService(db)
    try:
        customer = service.create_customer(customer_data)
        return customer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all customers with pagination
    """
    service = CustomerService(db)
    customers = service.list_customers(skip=skip, limit=limit)
    return customers

@router.get("/search/{query}")
async def search_customers(
    query: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search customers by name or phone
    """
    service = CustomerService(db)
    customers = service.search_customers(query)
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific customer by ID
    """
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update customer information
    """
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    updated_customer = service.update_customer(customer_id, customer_data)
    return updated_customer

@router.post("/{customer_id}/loyalty-card")
async def issue_loyalty_card(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Issue a loyalty card to a customer
    """
    service = CustomerService(db)
    try:
        card = service.issue_loyalty_card(customer_id)
        return card
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{customer_id}/loyalty-card")
async def get_loyalty_card(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get customer's loyalty card info
    """
    service = CustomerService(db)
    card = service.get_loyalty_card(customer_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer or loyalty card not found"
        )
    return card

@router.post("/{customer_id}/loyalty-card/add-points/{points}")
async def add_loyalty_points(
    customer_id: int,
    points: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add points to customer's loyalty card
    """
    service = CustomerService(db)
    try:
        card = service.add_loyalty_points(customer_id, points)
        return card
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{customer_id}/loyalty-card/redeem/{points}")
async def redeem_loyalty_points(
    customer_id: int,
    points: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Redeem loyalty points from customer's card
    """
    service = CustomerService(db)
    try:
        card = service.redeem_loyalty_points(customer_id, points)
        return card
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{customer_id}/stats")
async def get_customer_stats(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get customer statistics (total spending, visits, etc.)
    """
    service = CustomerService(db)
    stats = service.get_customer_stats(customer_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return stats
