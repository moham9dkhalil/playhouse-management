"""
API v1 Endpoints
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .devices import router as devices_router
from .sessions import router as sessions_router
from .customers import router as customers_router
from .sales import router as sales_router
from .reports import router as reports_router
from .products import router as products_router
from .settings import router as settings_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(devices_router)
api_router.include_router(sessions_router)
api_router.include_router(customers_router)
api_router.include_router(sales_router)
api_router.include_router(reports_router)
api_router.include_router(products_router)
api_router.include_router(settings_router)
