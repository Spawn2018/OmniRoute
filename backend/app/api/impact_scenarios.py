from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.impact_scenario import ImpactScenario
from app.services.impact_scenarios.impact_scenario_service import ImpactScenarioService

router = APIRouter(prefix="/impact-scenarios", tags=["impact-scenarios"])

_PERM = "can_manage_impact_scenarios"


class ImpactScenarioCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_code: str
    chain_label: str
    source_ref: str


class ImpactScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    scenario_code: str
    chain_label: str
    source_ref: str


def _row(saved: ImpactScenario) -> ImpactScenarioResponse:
    return ImpactScenarioResponse.model_validate(saved)


@router.get("", response_model=list[ImpactScenarioResponse])
async def list_impact_scenarios(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ImpactScenarioResponse]:
    packed = await ImpactScenarioService(session).list_scenarios()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ImpactScenarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_impact_scenario(
    body: ImpactScenarioCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ImpactScenarioResponse:
    saved = await ImpactScenarioService(session).persist_impact_scenario(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        scenario_code=body.scenario_code,
        chain_label=body.chain_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
