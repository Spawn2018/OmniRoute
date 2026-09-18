from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.blank_sailing_mark import BlankSailingMark
from app.services.blank_sailing_marks.blank_sailing_mark_service import (
    BlankSailingMarkService,
)

router = APIRouter(prefix="/blank-sailing-marks", tags=["blank-sailing-marks"])

_PERM = "can_manage_blank_sailing_marks"


class BlankSailingMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    sailing_kind: str
    source_ref: str


class BlankSailingMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    sailing_kind: str
    source_ref: str


def _row(saved: BlankSailingMark) -> BlankSailingMarkResponse:
    return BlankSailingMarkResponse.model_validate(saved)


@router.get("", response_model=list[BlankSailingMarkResponse])
async def list_blank_sailing_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BlankSailingMarkResponse]:
    packed = await BlankSailingMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=BlankSailingMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_blank_sailing_mark(
    body: BlankSailingMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BlankSailingMarkResponse:
    saved = await BlankSailingMarkService(session).persist_blank_sailing_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        sailing_kind=body.sailing_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
