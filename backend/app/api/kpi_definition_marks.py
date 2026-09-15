from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.kpi_definition_mark import KpiDefinitionMark
from app.services.kpi_definition_marks.kpi_definition_mark_service import (
    KpiDefinitionMarkService,
)

router = APIRouter(
    prefix="/kpi-definition-marks",
    tags=["kpi-definition-marks"],
)

_PERM = "can_manage_kpi_definition_marks"


class KpiDefinitionMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    kpi_kind: str
    source_ref: str


class KpiDefinitionMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    kpi_kind: str
    source_ref: str


def _row(saved: KpiDefinitionMark) -> KpiDefinitionMarkResponse:
    return KpiDefinitionMarkResponse.model_validate(saved)


@router.get("", response_model=list[KpiDefinitionMarkResponse])
async def list_kpi_definition_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[KpiDefinitionMarkResponse]:
    packed = await KpiDefinitionMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=KpiDefinitionMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_kpi_definition_mark(
    body: KpiDefinitionMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> KpiDefinitionMarkResponse:
    saved = await KpiDefinitionMarkService(session).persist_kpi_definition_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        kpi_kind=body.kpi_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
