"""
Play Sessions Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models import PlaySession, User, PlaystationDevice, Customer
from app.schemas import (
    PlaySessionCreate,
    PlaySessionUpdate,
    PlaySessionResponse,
    PlaySessionEndRequest
)
from app.services.session_service import SessionService
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=PlaySessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: PlaySessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start a new play session
    Can be started by staff or managers
    """
    service = SessionService(db)
    try:
        session = service.create_session(session_data, current_user.id)
        return session
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[PlaySessionResponse])
async def list_sessions(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all sessions with pagination
    Optionally filter by status (active, completed, paused)
    """
    service = SessionService(db)
    sessions = service.list_sessions(skip=skip, limit=limit, status=status_filter)
    return sessions

@router.get("/active", response_model=List[PlaySessionResponse])
async def get_active_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all currently active sessions
    """
    service = SessionService(db)
    sessions = service.get_active_sessions()
    return sessions

@router.get("/{session_id}", response_model=PlaySessionResponse)
async def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific session by ID
    """
    service = SessionService(db)
    session = service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session

@router.post("/{session_id}/pause")
async def pause_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Pause an active session
    """
    service = SessionService(db)
    try:
        session = service.pause_session(session_id)
        return session
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{session_id}/resume")
async def resume_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resume a paused session
    """
    service = SessionService(db)
    try:
        session = service.resume_session(session_id)
        return session
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{session_id}/end")
async def end_session(
    session_id: int,
    end_data: PlaySessionEndRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    End a session and calculate final billing
    """
    service = SessionService(db)
    try:
        session = service.end_session(session_id, end_data)
        return session
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/device/{device_id}/active")
async def get_device_active_session(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current active session on a device (if any)
    """
    service = SessionService(db)
    session = service.get_device_active_session(device_id)
    if not session:
        return {"message": "No active session on this device"}
    return session

@router.get("/customer/{customer_id}/history")
async def get_customer_session_history(
    customer_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get session history for a customer
    """
    service = SessionService(db)
    sessions = service.get_customer_sessions(customer_id, skip=skip, limit=limit)
    if sessions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return sessions
