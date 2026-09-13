"""HTTP ledger oszczędności — HITL method_label + Decimal, bez liczenia z charge."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.benefit_ledger import BenefitLedger
from app.services.benefit_ledgers.benefit_ledger_service import BenefitLedgerService

router = APIRouter(prefix="/benefit-ledgers", tags=["benefit-ledgers"])
_PERM = "can_manage_benefit_ledgers"


class BenefitLedgerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    benefit_code: str = Field(min_length=2, max_length=32)
    method_label: str = Field(min_length=1, max_length=256)
    hours_saved: str
    saved_amount: str
    saved_currency: str = Field(min_length=3, max_length=3)
    source_ref: str = Field(min_length=1, max_length=256)


class BenefitLedgerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    benefit_code: str
    method_label: str
    hours_saved: str
    saved_amount: str
    saved_currency: str
    source_ref: str


def _as_row(row: BenefitLedger) -> BenefitLedgerResponse:
    return BenefitLedgerResponse(
        id=row.id,
        organization_id=row.organization_id,
        benefit_code=row.benefit_code,
        method_label=row.method_label,
        hours_saved=format(row.hours_saved, "f"),
        saved_amount=format(row.saved_amount, "f"),
        saved_currency=row.saved_currency,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[BenefitLedgerResponse])
async def list_benefit_ledgers(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BenefitLedgerResponse]:
    rows = await BenefitLedgerService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=BenefitLedgerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_benefit_ledger(
    body: BenefitLedgerCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BenefitLedgerResponse:
    saved = await BenefitLedgerService(session).persist_ledger(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        benefit_code=body.benefit_code,
        method_label=body.method_label,
        hours_saved=body.hours_saved,
        saved_amount=body.saved_amount,
        saved_currency=body.saved_currency,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "benefit-ledger"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
