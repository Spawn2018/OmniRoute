from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.prediction_ledger import PredictionLedger
from app.services.prediction_ledgers.prediction_ledger_service import PredictionLedgerService

router = APIRouter(prefix="/prediction-ledgers", tags=["prediction-ledgers"])

_PERM = "can_manage_prediction_ledgers"


class PredictionLedgerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction_kind: str
    horizon_code: str
    interval_low: str
    interval_high: str
    crps: str
    mae: str
    model_code: str
    source_ref: str


class PredictionLedgerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    prediction_kind: str
    horizon_code: str
    interval_low: str
    interval_high: str
    crps: str
    mae: str
    model_code: str
    source_ref: str


def _as_row(row: PredictionLedger) -> PredictionLedgerResponse:
    return PredictionLedgerResponse(
        id=row.id,
        organization_id=row.organization_id,
        prediction_kind=row.prediction_kind,
        horizon_code=row.horizon_code,
        interval_low=format(row.interval_low, "f"),
        interval_high=format(row.interval_high, "f"),
        crps=format(row.crps, "f"),
        mae=format(row.mae, "f"),
        model_code=row.model_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[PredictionLedgerResponse])
async def list_prediction_ledgers(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PredictionLedgerResponse]:
    rows = await PredictionLedgerService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=PredictionLedgerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_prediction_ledger(
    body: PredictionLedgerCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PredictionLedgerResponse:
    row = await PredictionLedgerService(session).persist_ledger(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        prediction_kind=body.prediction_kind,
        horizon_code=body.horizon_code,
        interval_low=body.interval_low,
        interval_high=body.interval_high,
        crps=body.crps,
        mae=body.mae,
        model_code=body.model_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
