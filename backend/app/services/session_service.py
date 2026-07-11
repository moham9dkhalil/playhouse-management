"""
Session Service - Business Logic for Play Session Management
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal

from app.models import PlaySession, PlaystationDevice, Customer
from app.schemas import PlaySessionCreate, PlaySessionEndRequest


class SessionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_session(self, session_data: PlaySessionCreate, user_id: int) -> PlaySession:
        """Create a new play session"""
        # Validate device exists and is active
        device = self.db.query(PlaystationDevice).filter(
            PlaystationDevice.id == session_data.device_id
        ).first()
        
        if not device:
            raise ValueError("Device not found")
        
        if device.status != "active":
            raise ValueError(f"Device is {device.status}, cannot start session")
        
        # Check if device already has active session
        active = self.db.query(PlaySession).filter(
            and_(
                PlaySession.device_id == session_data.device_id,
                PlaySession.status == "active"
            )
        ).first()
        
        if active:
            raise ValueError("Device already has an active session")
        
        # Validate customer if provided
        customer = None
        if session_data.customer_id:
            customer = self.db.query(Customer).filter(
                Customer.id == session_data.customer_id
            ).first()
            
            if not customer:
                raise ValueError("Customer not found")
        
        db_session = PlaySession(
            device_id=session_data.device_id,
            customer_id=session_data.customer_id,
            started_at=datetime.utcnow(),
            status="active",
            hourly_rate=session_data.hourly_rate or 50.0,  # Default rate
            created_by=user_id
        )
        
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session
    
    def list_sessions(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[PlaySession]:
        """Get all sessions with optional status filter"""
        query = self.db.query(PlaySession)
        
        if status:
            query = query.filter(PlaySession.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def get_active_sessions(self) -> List[PlaySession]:
        """Get all currently active sessions"""
        return self.db.query(PlaySession).filter(
            PlaySession.status == "active"
        ).all()
    
    def get_session(self, session_id: int) -> Optional[PlaySession]:
        """Get a specific session"""
        return self.db.query(PlaySession).filter(
            PlaySession.id == session_id
        ).first()
    
    def pause_session(self, session_id: int) -> PlaySession:
        """Pause an active session"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        if session.status != "active":
            raise ValueError(f"Cannot pause a {session.status} session")
        
        session.status = "paused"
        session.paused_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def resume_session(self, session_id: int) -> PlaySession:
        """Resume a paused session"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        if session.status != "paused":
            raise ValueError(f"Cannot resume a {session.status} session")
        
        # Add paused time to total paused duration
        if session.paused_at:
            pause_duration = datetime.utcnow() - session.paused_at
            session.total_paused_duration = (session.total_paused_duration or timedelta(0)) + pause_duration
        
        session.status = "active"
        session.paused_at = None
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def end_session(self, session_id: int, end_data: PlaySessionEndRequest) -> PlaySession:
        """End a session and calculate billing"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        if session.status not in ["active", "paused"]:
            raise ValueError(f"Cannot end a {session.status} session")
        
        # Calculate duration
        ended_at = datetime.utcnow()
        total_duration = ended_at - session.started_at
        
        # Subtract paused time
        paused_duration = session.total_paused_duration or timedelta(0)
        if session.paused_at:
            paused_duration += datetime.utcnow() - session.paused_at
        
        active_duration = total_duration - paused_duration
        
        # Calculate cost
        hours = active_duration.total_seconds() / 3600
        session_cost = Decimal(str(hours)) * Decimal(str(session.hourly_rate))
        
        # Add extras if provided
        if end_data.extra_cost:
            session_cost += Decimal(str(end_data.extra_cost))
        
        session.ended_at = ended_at
        session.status = "completed"
        session.total_duration = total_duration
        session.active_duration = active_duration
        session.total_cost = session_cost
        session.notes = end_data.notes
        
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_device_active_session(self, device_id: int) -> Optional[PlaySession]:
        """Get the current active session on a device"""
        return self.db.query(PlaySession).filter(
            and_(
                PlaySession.device_id == device_id,
                PlaySession.status == "active"
            )
        ).first()
    
    def get_customer_sessions(self, customer_id: int, skip: int = 0, limit: int = 50) -> Optional[List[PlaySession]]:
        """Get all sessions for a customer"""
        # Check customer exists
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return None
        
        return self.db.query(PlaySession).filter(
            PlaySession.customer_id == customer_id
        ).order_by(PlaySession.started_at.desc()).offset(skip).limit(limit).all()
