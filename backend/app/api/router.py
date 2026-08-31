from fastapi import APIRouter

from app.api import extractions, session, table_views, tenancy
from app.domain.errors import PermissionDenied

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(session.router)
api_router.include_router(tenancy.router)
api_router.include_router(table_views.router)
api_router.include_router(extractions.router)


@api_router.api_route(
    "/{undeclared_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    include_in_schema=False,
)
async def deny_undeclared_path(undeclared_path: str) -> None:
    _ = undeclared_path
    raise PermissionDenied("Brak deklaracji uprawnień")
