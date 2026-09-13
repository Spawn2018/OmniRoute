"""Odczyt średnich MAE/CRPS per wersja i dzień UTC — liczy Postgres."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission, require_tenant_session
from app.models.version_window import VersionWindow
from app.services.version_windows.version_window_service import VersionWindowService

router = APIRouter(prefix="/version-windows", tags=["version-windows"])
_PERM = "can_manage_version_windows"
_SCALE = Decimal("0.0001")


class VersionWindowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization_id: UUID
    model_version: str
    created_on: date
    pair_count: int
    avg_mae: str
    avg_crps: str


def _stamp(value: Decimal) -> str:
    return format(value.quantize(_SCALE), "f")


def _as_row(row: VersionWindow) -> VersionWindowResponse:
    return VersionWindowResponse(
        organization_id=row.organization_id,
        model_version=row.model_version,
        created_on=row.created_on,
        pair_count=row.pair_count,
        avg_mae=_stamp(row.avg_mae),
        avg_crps=_stamp(row.avg_crps),
    )


@router.post("", include_in_schema=False)
async def reject_version_window_write() -> None:
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="wynik okna wersji jest tylko odczytem",
    )


@router.get("", response_model=list[VersionWindowResponse])
async def list_version_windows(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[VersionWindowResponse]:
    rows = await VersionWindowService(session).list_rows()
    return [_as_row(row) for row in rows]
