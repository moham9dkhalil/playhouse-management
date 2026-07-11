"""SQLAlchemy Models"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Numeric, Date, Interval
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(50), default="staff")  # admin, manager, staff
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    devices = relationship("PlaystationDevice", back_populates="creator")
    sessions = relationship("PlaySession", back_populates="creator")

class PlaystationDevice(Base):
    __tablename__ = "playstation_device"
    
    id = Column(Integer, primary_key=True)
    device_name = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True, index=True, nullable=False)
    console_type = Column(String(50), nullable=False)
    location = Column(String(200), nullable=False)
    status = Column(String(50), default="active")
    maintenance_notes = Column(Text)
    last_maintenance = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    creator = relationship("User", back_populates="devices")
    sessions = relationship("PlaySession", back_populates="device")

class PlaySession(Base):
    __tablename__ = "play_session"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("playstation_device.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    paused_at = Column(DateTime)
    status = Column(String(50), default="active")
    hourly_rate = Column(Float, default=50.0)
    total_duration = Column(Interval)
    active_duration = Column(Interval)
    total_paused_duration = Column(Interval)
    total_cost = Column(Numeric(10, 2))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    device = relationship("PlaystationDevice", back_populates="sessions")
    customer = relationship("Customer", back_populates="sessions")
    creator = relationship("User", back_populates="sessions")

class Customer(Base):
    __tablename__ = "customer"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100))
    date_of_birth = Column(Date)
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sessions = relationship("PlaySession", back_populates="customer")
    loyalty_card = relationship("LoyaltyCard", back_populates="customer", uselist=False)

class LoyaltyCard(Base):
    __tablename__ = "loyalty_card"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), unique=True, nullable=False)
    card_number = Column(String(50), unique=True, index=True, nullable=False)
    points_balance = Column(Integer, default=0)
    issued_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="loyalty_card")

class CafeteriaProduct(Base):
    __tablename__ = "cafeteria_product"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sale_items = relationship("SaleItem", back_populates="product")

class Sale(Base):
    __tablename__ = "sale"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    total_amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    __tablename__ = "sale_item"
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sale.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("cafeteria_product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    sale = relationship("Sale", back_populates="items")
    product = relationship("CafeteriaProduct", back_populates="sale_items")

class Game(Base):
    __tablename__ = "game"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    genre = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
