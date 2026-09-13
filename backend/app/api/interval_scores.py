"""Odczyt MAE/CRPS ze złączenia ledgerów — liczy Postgres, nie body."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission, require_tenant_session
from app.models.interval_score import IntervalScore
from app.services.interval_scores.interval_score_service import IntervalScoreService

router = APIRouter(prefix="/interval-scores", tags=["interval-scores"])
_PERM = "can_manage_interval_scores"
_SCALE = Decimal("0.0001")


class IntervalScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization_id: UUID
    outcome_id: UUID
    suggestion_id: UUID
    entity_id: UUID
    interval_low: str
    interval_high: str
    actual_value: str
    mae: str
    crps: str


def _stamp(value: Decimal) -> str:
    return format(value.quantize(_SCALE), "f")


def _as_row(row: IntervalScore) -> IntervalScoreResponse:
    return IntervalScoreResponse(
        organization_id=row.organization_id,
        outcome_id=row.outcome_id,
        suggestion_id=row.suggestion_id,
        entity_id=row.entity_id,
        interval_low=_stamp(row.interval_low),
        interval_high=_stamp(row.interval_high),
        actual_value=_stamp(row.actual_value),
        mae=_stamp(row.mae),
        crps=_stamp(row.crps),
    )


@router.post("", include_in_schema=False)
async def reject_interval_score_write() -> None:
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="wynik przedziału jest tylko odczytem",
    )


@router.get("", response_model=list[IntervalScoreResponse])
async def list_interval_scores(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[IntervalScoreResponse]:
    rows = await IntervalScoreService(session).list_rows()
    return [_as_row(row) for row in rows]
