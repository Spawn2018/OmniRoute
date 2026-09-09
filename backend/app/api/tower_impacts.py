from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.tower_impact import contract_gap_label
from app.models.tower_impact import TowerImpact
from app.services.tower_impacts.tower_impact_service import (
    TowerImpactService,
)

router = APIRouter(prefix="/tower-impacts", tags=["tower-impacts"])

_PERM = "can_manage_tower_impacts"


class TowerImpactCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chain_stage: str
    contract_data_status: str
    source_ref: str


class TowerImpactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    chain_stage: str
    contract_data_status: str
    source_ref: str
    contract_gap_label: str | None


def _as_row(row: TowerImpact) -> TowerImpactResponse:
    return TowerImpactResponse(
        id=row.id,
        organization_id=row.organization_id,
        chain_stage=row.chain_stage,
        contract_data_status=row.contract_data_status,
        source_ref=row.source_ref,
        contract_gap_label=contract_gap_label(row.contract_data_status),
    )


@router.get("", response_model=list[TowerImpactResponse])
async def list_tower_impacts(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TowerImpactResponse]:
    rows = await TowerImpactService(session).list_marks()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TowerImpactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tower_impact(
    body: TowerImpactCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TowerImpactResponse:
    row = await TowerImpactService(session).persist_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        chain_stage=body.chain_stage,
        contract_data_status=body.contract_data_status,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
