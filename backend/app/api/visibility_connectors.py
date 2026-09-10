from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.visibility_connector import VisibilityConnector
from app.services.visibility_connectors.visibility_connector_service import (
    VisibilityConnectorService,
)

router = APIRouter(prefix="/visibility-connectors", tags=["visibility-connectors"])

_PERM = "can_manage_visibility_connectors"


class VisibilityConnectorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connector_code: str
    system_kind: str
    source_ref: str


class VisibilityConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connector_code: str
    system_kind: str
    source_ref: str


def _row(saved: VisibilityConnector) -> VisibilityConnectorResponse:
    return VisibilityConnectorResponse.model_validate(saved)


@router.get("", response_model=list[VisibilityConnectorResponse])
async def list_visibility_connectors(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[VisibilityConnectorResponse]:
    packed = await VisibilityConnectorService(session).list_fixtures()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=VisibilityConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_visibility_connector(
    body: VisibilityConnectorCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> VisibilityConnectorResponse:
    saved = await VisibilityConnectorService(session).persist_visibility_fixture(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        connector_code=body.connector_code,
        system_kind=body.system_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
