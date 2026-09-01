from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.geography.terminal_service import TerminalService

router = APIRouter(prefix="/terminals", tags=["terminals"])

_GEOGRAPHY = require_permission("can_manage_geography", "organization")


class TerminalCreate(BaseModel):
    port_id: UUID
    name: str = Field(min_length=1, max_length=128)
    isps_code: str | None = Field(default=None, max_length=32)
    operator_name: str | None = Field(default=None, max_length=256)
    lat: Decimal | None = None
    lng: Decimal | None = None


class TerminalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    port_id: UUID
    name: str
    isps_code: str | None
    operator_name: str | None
    lat: Decimal | None
    lng: Decimal | None
    source_ref: str


@router.get("", response_model=list[TerminalResponse])
async def list_terminals(
    port_id: UUID | None = Query(default=None),
    search: str | None = Query(default=None, max_length=128),
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TerminalResponse]:
    rows = await TerminalService(session).list_terminals(port_id=port_id, search=search)
    return [TerminalResponse.model_validate(row) for row in rows]


@router.get("/resolve", response_model=TerminalResponse)
async def resolve_terminal(
    isps_code: str = Query(..., min_length=1, max_length=32),
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
) -> TerminalResponse:
    row = await TerminalService(session).resolve(isps_code)
    return TerminalResponse.model_validate(row)


@router.post("", response_model=TerminalResponse, status_code=status.HTTP_201_CREATED)
async def create_terminal(
    body: TerminalCreate,
    _authz: None = Depends(_GEOGRAPHY),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TerminalResponse:
    row = await TerminalService(session).create_terminal(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        port_id=body.port_id,
        name=body.name,
        isps_code=body.isps_code,
        operator_name=body.operator_name,
        lat=body.lat,
        lng=body.lng,
    )
    await session.commit()
    return TerminalResponse.model_validate(row)
