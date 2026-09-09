from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.monitoring_scheme import MonitoringScheme
from app.services.monitoring_schemes.monitoring_scheme_service import (
    MonitoringSchemeService,
)

router = APIRouter(prefix="/monitoring-schemes", tags=["monitoring-schemes"])

_PERM = "can_manage_monitoring_schemes"


class MonitoringSchemeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scheme_code: str
    source_ref: str


class MonitoringSchemeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    scheme_code: str
    source_ref: str


def _as_row(row: MonitoringScheme) -> MonitoringSchemeResponse:
    return MonitoringSchemeResponse(
        id=row.id,
        organization_id=row.organization_id,
        scheme_code=row.scheme_code,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[MonitoringSchemeResponse])
async def list_monitoring_schemes(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MonitoringSchemeResponse]:
    rows = await MonitoringSchemeService(session).list_schemes()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=MonitoringSchemeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_monitoring_scheme(
    body: MonitoringSchemeCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MonitoringSchemeResponse:
    row = await MonitoringSchemeService(session).persist_scheme(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        scheme_code=body.scheme_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
