from fastapi import APIRouter

from app.api import (
    charge_codes,
    charges,
    extractions,
    locations,
    organization_settings,
    ports,
    quotations,
    rate_lines,
    session,
    table_views,
    tenancy,
)
from app.domain.errors import PermissionDenied

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(session.router)
api_router.include_router(tenancy.router)
api_router.include_router(table_views.router)
api_router.include_router(extractions.router)
api_router.include_router(charge_codes.router)
api_router.include_router(charges.router)
api_router.include_router(rate_lines.router)
api_router.include_router(quotations.router)
api_router.include_router(organization_settings.router)
api_router.include_router(ports.router)
api_router.include_router(locations.router)


@api_router.api_route(
    "/{undeclared_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    include_in_schema=False,
)
async def deny_undeclared_path(undeclared_path: str) -> None:
    _ = undeclared_path
    raise PermissionDenied("Brak deklaracji uprawnień")
