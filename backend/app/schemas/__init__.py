"""
Pydantic Schemas for Request/Response Validation
"""
from .auth import UserRegister, UserLogin, TokenResponse, UserResponse
from .devices import PlaystationDeviceCreate, PlaystationDeviceUpdate, PlaystationDeviceResponse
from .sessions import (
    PlaySessionCreate,
    PlaySessionUpdate,
    PlaySessionResponse,
    PlaySessionEndRequest
)
from .customers import CustomerCreate, CustomerUpdate, CustomerResponse
from .sales import SaleCreate, SaleResponse, SaleItemCreate

__all__ = [
    # Auth
    "UserRegister",
    "UserLogin",
    "TokenResponse",
    "UserResponse",
    # Devices
    "PlaystationDeviceCreate",
    "PlaystationDeviceUpdate",
    "PlaystationDeviceResponse",
    # Sessions
    "PlaySessionCreate",
    "PlaySessionUpdate",
    "PlaySessionResponse",
    "PlaySessionEndRequest",
    # Customers
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    # Sales
    "SaleCreate",
    "SaleResponse",
    "SaleItemCreate",
]
