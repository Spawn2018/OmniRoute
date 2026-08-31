from fastapi import APIRouter

from app.api import extractions, session, table_views, tenancy

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(session.router)
api_router.include_router(tenancy.router)
api_router.include_router(table_views.router)
api_router.include_router(extractions.router)
