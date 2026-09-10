from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.exchange_connector import ExchangeConnector
from app.services.exchange_connectors.exchange_connector_service import ExchangeConnectorService

router = APIRouter(prefix="/exchange-connectors", tags=["exchange-connectors"])

_PERM = "can_manage_exchange_connectors"


class ExchangeConnectorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connector_code: str
    system_kind: str
    source_ref: str


class ExchangeConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connector_code: str
    system_kind: str
    source_ref: str


def _as_row(row: ExchangeConnector) -> ExchangeConnectorResponse:
    return ExchangeConnectorResponse(
        id=row.id,
        organization_id=row.organization_id,
        connector_code=row.connector_code,
        system_kind=row.system_kind,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[ExchangeConnectorResponse])
async def list_exchange_connectors(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ExchangeConnectorResponse]:
    rows = await ExchangeConnectorService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=ExchangeConnectorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_exchange_connector(
    body: ExchangeConnectorCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ExchangeConnectorResponse:
    row = await ExchangeConnectorService(session).persist_exchange_connector(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        connector_code=body.connector_code,
        system_kind=body.system_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
