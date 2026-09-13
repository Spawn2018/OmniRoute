"""Odczyt średnich MAE/CRPS per wersja modelu — liczy Postgres."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission, require_tenant_session
from app.models.version_score import VersionScore
from app.services.version_scores.version_score_service import VersionScoreService

router = APIRouter(prefix="/version-scores", tags=["version-scores"])
_PERM = "can_manage_version_scores"
_SCALE = Decimal("0.0001")


class VersionScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization_id: UUID
    model_version: str
    pair_count: int
    avg_mae: str
    avg_crps: str


def _stamp(value: Decimal) -> str:
    return format(value.quantize(_SCALE), "f")


def _as_row(row: VersionScore) -> VersionScoreResponse:
    return VersionScoreResponse(
        organization_id=row.organization_id,
        model_version=row.model_version,
        pair_count=row.pair_count,
        avg_mae=_stamp(row.avg_mae),
        avg_crps=_stamp(row.avg_crps),
    )


@router.post("", include_in_schema=False)
async def reject_version_score_write() -> None:
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="wynik wersji jest tylko odczytem",
    )


@router.get("", response_model=list[VersionScoreResponse])
async def list_version_scores(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[VersionScoreResponse]:
    rows = await VersionScoreService(session).list_rows()
    return [_as_row(row) for row in rows]
