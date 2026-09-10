from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.idp_connector import IdpConnector
from app.services.idp_connectors.idp_connector_service import IdpConnectorService

router = APIRouter(prefix="/idp-connectors", tags=["idp-connectors"])

_PERM = "can_manage_idp_connectors"


class IdpConnectorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connector_code: str
    provider_code: str
    source_ref: str
    public_domain: str | None = None


class IdpConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connector_code: str
    provider_code: str
    public_domain: str | None
    source_ref: str


def _as_row(row: IdpConnector) -> IdpConnectorResponse:
    return IdpConnectorResponse(
        id=row.id,
        organization_id=row.organization_id,
        connector_code=row.connector_code,
        provider_code=row.provider_code,
        public_domain=row.public_domain,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[IdpConnectorResponse])
async def list_idp_connectors(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[IdpConnectorResponse]:
    rows = await IdpConnectorService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=IdpConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_idp_connector(
    body: IdpConnectorCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> IdpConnectorResponse:
    row = await IdpConnectorService(session).persist_idp_connector(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        connector_code=body.connector_code,
        provider_code=body.provider_code,
        source_ref=body.source_ref,
        public_domain=body.public_domain,
    )
    await session.commit()
    return _as_row(row)
