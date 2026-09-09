from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.telematics_connector import TelematicsConnector
from app.services.telematics_connectors.telematics_connector_service import (
    TelematicsConnectorService,
)

router = APIRouter(prefix="/telematics-connectors", tags=["telematics-connectors"])

_PERM = "can_manage_telematics_connectors"


class TelematicsConnectorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    observation_kind: str
    provider_code: str
    source_ref: str


class TelematicsConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    observation_kind: str
    provider_code: str
    source_ref: str


def _as_row(row: TelematicsConnector) -> TelematicsConnectorResponse:
    return TelematicsConnectorResponse.model_validate(row)


@router.get("", response_model=list[TelematicsConnectorResponse])
async def list_telematics_connectors(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TelematicsConnectorResponse]:
    rows = await TelematicsConnectorService(session).list_marks()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=TelematicsConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_telematics_connector(
    body: TelematicsConnectorCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TelematicsConnectorResponse:
    row = await TelematicsConnectorService(session).persist_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        observation_kind=body.observation_kind,
        provider_code=body.provider_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
