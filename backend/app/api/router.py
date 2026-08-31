from fastapi import APIRouter

from app.api import tenancy

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(tenancy.router)
