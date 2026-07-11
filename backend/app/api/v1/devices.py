"""
Devices Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models import PlaystationDevice, User
from app.schemas import (
    PlaystationDeviceCreate,
    PlaystationDeviceUpdate,
    PlaystationDeviceResponse
)
from app.services.device_service import DeviceService
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/devices", tags=["devices"])

@router.post("/", response_model=PlaystationDeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    device_data: PlaystationDeviceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new PlayStation device
    Only managers and admins can create devices
    """
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can create devices"
        )
    
    service = DeviceService(db)
    try:
        device = service.create_device(device_data, current_user.id)
        return device
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[PlaystationDeviceResponse])
async def list_devices(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all devices with pagination
    Optionally filter by status (active, maintenance, inactive)
    """
    service = DeviceService(db)
    devices = service.list_devices(skip=skip, limit=limit, status=status_filter)
    return devices

@router.get("/{device_id}", response_model=PlaystationDeviceResponse)
async def get_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific device by ID
    """
    service = DeviceService(db)
    device = service.get_device(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    return device

@router.put("/{device_id}", response_model=PlaystationDeviceResponse)
async def update_device(
    device_id: int,
    device_data: PlaystationDeviceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a device
    Only managers and admins can update devices
    """
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can update devices"
        )
    
    service = DeviceService(db)
    device = service.get_device(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    try:
        updated_device = service.update_device(device_id, device_data)
        return updated_device
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a device (soft delete)
    Only admins can delete devices
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete devices"
        )
    
    service = DeviceService(db)
    device = service.get_device(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    service.delete_device(device_id)

@router.post("/{device_id}/maintenance")
async def mark_maintenance(
    device_id: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a device as under maintenance
    """
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can mark devices for maintenance"
        )
    
    service = DeviceService(db)
    try:
        device = service.mark_maintenance(device_id, reason)
        return device
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/{device_id}/activate")
async def activate_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activate a device (mark as active)
    """
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can activate devices"
        )
    
    service = DeviceService(db)
    try:
        device = service.activate_device(device_id)
        return device
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/{device_id}/sessions")
async def get_device_sessions(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all sessions for a specific device
    """
    service = DeviceService(db)
    sessions = service.get_device_sessions(device_id)
    if sessions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    return sessions
