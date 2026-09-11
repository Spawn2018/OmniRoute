from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.yard_mark import YardMark
from app.services.yard_marks.yard_mark_service import YardMarkService

router = APIRouter(prefix="/yard-marks", tags=["yard-marks"])

_PERM = "can_manage_yard_marks"


class YardMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    yard_kind: str
    source_ref: str


class YardMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    yard_kind: str
    source_ref: str


def _row(saved: YardMark) -> YardMarkResponse:
    return YardMarkResponse.model_validate(saved)


@router.get("", response_model=list[YardMarkResponse])
async def list_yard_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[YardMarkResponse]:
    packed = await YardMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=YardMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_yard_mark(
    body: YardMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> YardMarkResponse:
    saved = await YardMarkService(session).persist_yard_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        yard_kind=body.yard_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
