from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.operator_notices.operator_notice_service import OperatorNoticeService

router = APIRouter(prefix="/operator-notices", tags=["operator-notices"])

_AUTHZ = require_permission("can_manage_operator_notices", "organization")


class OperatorNoticeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: str
    source_ref: str
    kind: str | None = None


class OperatorNoticeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    kind: str
    body: str
    status: str
    read_at: datetime | None
    source_ref: str


@router.get("", response_model=list[OperatorNoticeResponse])
async def list_operator_notices(
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OperatorNoticeResponse]:
    rows = await OperatorNoticeService(session).list_notices()
    return [OperatorNoticeResponse.model_validate(row) for row in rows]


@router.post("", response_model=OperatorNoticeResponse, status_code=status.HTTP_201_CREATED)
async def create_operator_notice(
    body: OperatorNoticeCreate,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OperatorNoticeResponse:
    row = await OperatorNoticeService(session).create_notice(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        body=body.body,
        source_ref=body.source_ref,
        kind=body.kind,
    )
    await session.commit()
    return OperatorNoticeResponse.model_validate(row)


@router.post("/{notice_id}/read", response_model=OperatorNoticeResponse)
async def read_operator_notice(
    notice_id: UUID,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> OperatorNoticeResponse:
    row = await OperatorNoticeService(session).mark_read(notice_id)
    await session.commit()
    return OperatorNoticeResponse.model_validate(row)
