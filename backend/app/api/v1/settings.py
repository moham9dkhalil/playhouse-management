"""
Settings Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.models import SystemSettings, User
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/")
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all system settings
    """
    settings = db.query(SystemSettings).all()
    return {s.key: s.value for s in settings}

@router.post("/{key}")
async def update_setting(
    key: str,
    value: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a system setting
    Only admins can update settings
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update settings"
        )
    
    setting = db.query(SystemSettings).filter(SystemSettings.key == key).first()
    if not setting:
        setting = SystemSettings(key=key, value=value)
        db.add(setting)
    else:
        setting.value = value
    
    db.commit()
    db.refresh(setting)
    return {"key": setting.key, "value": setting.value}

@router.get("/{key}")
async def get_setting(
    key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific system setting
    """
    setting = db.query(SystemSettings).filter(SystemSettings.key == key).first()
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting '{key}' not found"
        )
    return {"key": setting.key, "value": setting.value}
