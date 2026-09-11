from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.intervention_outcome import InterventionOutcome
from app.services.intervention_outcomes.intervention_outcome_service import (
    InterventionOutcomeService,
)

router = APIRouter(prefix="/intervention-outcomes", tags=["intervention-outcomes"])

_PERM = "can_manage_intervention_outcomes"


class InterventionOutcomeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    outcome_code: str
    result_kind: str
    source_ref: str


class InterventionOutcomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    outcome_code: str
    result_kind: str
    source_ref: str


def _outcome(saved: InterventionOutcome) -> InterventionOutcomeResponse:
    return InterventionOutcomeResponse.model_validate(saved)


@router.get("", response_model=list[InterventionOutcomeResponse])
async def list_intervention_outcomes(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InterventionOutcomeResponse]:
    packed = await InterventionOutcomeService(session).list_outcomes()
    return [_outcome(item) for item in packed]


@router.post(
    "",
    response_model=InterventionOutcomeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_intervention_outcome(
    body: InterventionOutcomeCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InterventionOutcomeResponse:
    saved = await InterventionOutcomeService(session).persist_intervention_outcome(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        outcome_code=body.outcome_code,
        result_kind=body.result_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _outcome(saved)
