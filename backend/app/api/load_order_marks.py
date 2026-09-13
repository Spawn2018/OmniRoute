from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.load_order_mark import LoadOrderMark
from app.services.load_order_marks.load_order_mark_service import LoadOrderMarkService

router = APIRouter(prefix="/load-order-marks", tags=["load-order-marks"])

_PERM = "can_manage_load_order_marks"


class LoadOrderMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    order_kind: str
    source_ref: str


class LoadOrderMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    order_kind: str
    source_ref: str


def _row(saved: LoadOrderMark) -> LoadOrderMarkResponse:
    return LoadOrderMarkResponse.model_validate(saved)


@router.get("", response_model=list[LoadOrderMarkResponse])
async def list_load_order_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LoadOrderMarkResponse]:
    packed = await LoadOrderMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=LoadOrderMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_load_order_mark(
    body: LoadOrderMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LoadOrderMarkResponse:
    saved = await LoadOrderMarkService(session).persist_load_order_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        order_kind=body.order_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
