from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.sla_clause import SlaClause
from app.services.sla_clauses.sla_clause_service import SlaClauseService

router = APIRouter(prefix="/sla-clauses", tags=["sla-clauses"])

_PERM = "can_manage_sla_clauses"


class SlaClauseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_contract_id: UUID
    clause_code: str
    metric_kind: str
    threshold_label: str
    source_ref: str


class SlaClauseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    customer_contract_id: UUID
    clause_code: str
    metric_kind: str
    threshold_label: str
    source_ref: str


def _clause(saved: SlaClause) -> SlaClauseResponse:
    return SlaClauseResponse.model_validate(saved)


@router.get("", response_model=list[SlaClauseResponse])
async def list_sla_clauses(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SlaClauseResponse]:
    packed = await SlaClauseService(session).list_clauses()
    return [_clause(item) for item in packed]


@router.post(
    "",
    response_model=SlaClauseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sla_clause(
    body: SlaClauseCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SlaClauseResponse:
    saved = await SlaClauseService(session).persist_sla_clause(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        customer_contract_id=body.customer_contract_id,
        clause_code=body.clause_code,
        metric_kind=body.metric_kind,
        threshold_label=body.threshold_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _clause(saved)
