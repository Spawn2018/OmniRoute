from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.sap_connector import SapConnector
from app.services.sap_connectors.sap_connector_service import SapConnectorService

router = APIRouter(prefix="/sap-connectors", tags=["sap-connectors"])

_PERM = "can_manage_sap_connectors"


class SapConnectorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connector_code: str
    system_kind: str
    source_ref: str


class SapConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connector_code: str
    system_kind: str
    source_ref: str


def _connector(saved: SapConnector) -> SapConnectorResponse:
    return SapConnectorResponse.model_validate(saved)


@router.get("", response_model=list[SapConnectorResponse])
async def list_sap_connectors(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SapConnectorResponse]:
    packed = await SapConnectorService(session).list_connectors()
    return [_connector(item) for item in packed]


@router.post(
    "",
    response_model=SapConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sap_connector(
    body: SapConnectorCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SapConnectorResponse:
    saved = await SapConnectorService(session).persist_sap_connector(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        connector_code=body.connector_code,
        system_kind=body.system_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _connector(saved)
