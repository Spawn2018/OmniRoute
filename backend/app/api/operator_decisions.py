from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.operator_decisions.operator_decision_service import OperatorDecisionService

router = APIRouter(prefix="/operator-decisions", tags=["operator-decisions"])

_AUTHZ = require_permission("can_manage_operator_decisions", "organization")


class OperatorDecisionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_kind: str
    subject_id: UUID
    source_ref: str


class OperatorDecisionDecide(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str


class OperatorDecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    subject_kind: str
    subject_id: UUID
    status: str
    decided_at: datetime | None
    source_ref: str


@router.get("", response_model=list[OperatorDecisionResponse])
async def list_operator_decisions(
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OperatorDecisionResponse]:
    rows = await OperatorDecisionService(session).list_decisions()
    return [OperatorDecisionResponse.model_validate(row) for row in rows]


@router.post("", response_model=OperatorDecisionResponse, status_code=status.HTTP_201_CREATED)
async def create_operator_decision(
    body: OperatorDecisionCreate,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OperatorDecisionResponse:
    row = await OperatorDecisionService(session).create_decision(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_kind=body.subject_kind,
        subject_id=body.subject_id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return OperatorDecisionResponse.model_validate(row)


@router.post("/{decision_id}/decide", response_model=OperatorDecisionResponse)
async def decide_operator_decision(
    decision_id: UUID,
    body: OperatorDecisionDecide,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> OperatorDecisionResponse:
    row = await OperatorDecisionService(session).decide(decision_id, body.status)
    await session.commit()
    return OperatorDecisionResponse.model_validate(row)
