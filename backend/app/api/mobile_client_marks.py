"""HTTP katalog klienta mobilnego — HITL, bez Expo/EAS i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.mobile_client_mark import MobileClientMark
from app.services.mobile_client_marks.mobile_client_mark_service import MobileClientMarkService

router = APIRouter(prefix="/mobile-client-marks", tags=["mobile-client-mark"])
_PERM = "can_manage_mobile_client_marks"


class MobileClientMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    client_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class MobileClientMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    client_kind: str
    source_ref: str


def _to_dto(row: MobileClientMark) -> MobileClientMarkResponse:
    return MobileClientMarkResponse.model_validate(row)


@router.get("", response_model=list[MobileClientMarkResponse])
async def list_mobile_client_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MobileClientMarkResponse]:
    catalog = MobileClientMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=MobileClientMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_mobile_client_mark(
    body: MobileClientMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MobileClientMarkResponse:
    catalog = MobileClientMarkService(session)
    saved = await catalog.persist_mobile_client_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        client_kind=body.client_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "mobile-client-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
