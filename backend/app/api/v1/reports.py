"""
Statistics & Reports API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.models import User, PlaySession, Sale, Customer
from app.core.database import get_db
from app.core.security import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/daily-summary")
async def get_daily_summary(
    date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get daily summary statistics
    """
    if not date:
        target_date = datetime.utcnow().date()
    else:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    start = datetime.combine(target_date, datetime.min.time())
    end = datetime.combine(target_date, datetime.max.time())
    
    # Sessions stats
    sessions = db.query(PlaySession).filter(
        (PlaySession.started_at >= start) & (PlaySession.started_at <= end)
    ).all()
    
    total_sessions = len(sessions)
    total_revenue_sessions = sum(s.total_cost or 0 for s in sessions)
    
    # Sales stats
    sales = db.query(Sale).filter(
        (Sale.created_at >= start) & (Sale.created_at <= end)
    ).all()
    
    total_sales = len(sales)
    total_revenue_sales = sum(s.total_amount or 0 for s in sales)
    
    return {
        "date": target_date.isoformat(),
        "sessions": {
            "total": total_sessions,
            "revenue": float(total_revenue_sessions)
        },
        "sales": {
            "total": total_sales,
            "revenue": float(total_revenue_sales)
        },
        "total_revenue": float(total_revenue_sessions + total_revenue_sales)
    }

@router.get("/monthly-summary")
async def get_monthly_summary(
    month: Optional[int] = None,
    year: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get monthly summary statistics
    """
    now = datetime.utcnow()
    if not month:
        month = now.month
    if not year:
        year = now.year
    
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Sessions stats
    sessions = db.query(PlaySession).filter(
        (PlaySession.started_at >= start) & (PlaySession.started_at <= end)
    ).all()
    
    total_sessions = len(sessions)
    total_revenue_sessions = sum(s.total_cost or 0 for s in sessions)
    
    # Sales stats
    sales = db.query(Sale).filter(
        (Sale.created_at >= start) & (Sale.created_at <= end)
    ).all()
    
    total_sales = len(sales)
    total_revenue_sales = sum(s.total_amount or 0 for s in sales)
    
    return {
        "month": f"{year}-{month:02d}",
        "sessions": {
            "total": total_sessions,
            "revenue": float(total_revenue_sessions),
            "avg_per_session": float(total_revenue_sessions / total_sessions) if total_sessions > 0 else 0
        },
        "sales": {
            "total": total_sales,
            "revenue": float(total_revenue_sales),
            "avg_per_sale": float(total_revenue_sales / total_sales) if total_sales > 0 else 0
        },
        "total_revenue": float(total_revenue_sessions + total_revenue_sales)
    }

@router.get("/top-customers")
async def get_top_customers(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get top customers by spending
    """
    customers = db.query(
        Customer,
        func.count(PlaySession.id).label('sessions'),
        func.sum(PlaySession.total_cost).label('total_spent')
    ).join(PlaySession).group_by(Customer.id).order_by(
        func.sum(PlaySession.total_cost).desc()
    ).limit(limit).all()
    
    return [
        {
            "customer_id": c[0].id,
            "name": c[0].name,
            "phone": c[0].phone_number,
            "sessions": c[1],
            "total_spent": float(c[2] or 0)
        }
        for c in customers
    ]
