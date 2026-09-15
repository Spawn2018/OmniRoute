from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.sales_bind_mark import SalesBindMark
from app.services.sales_bind_marks.sales_bind_mark_service import SalesBindMarkService

router = APIRouter(prefix="/sales-bind-marks", tags=["sales-bind-marks"])


class SalesBindMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    bind_kind: str
    source_ref: str


class SalesBindMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    bind_kind: str
    source_ref: str


def _as_response(row: SalesBindMark) -> SalesBindMarkResponse:
    return SalesBindMarkResponse.model_validate(row)


@router.get("", response_model=list[SalesBindMarkResponse])
async def list_sales_bind_marks(
    _authz: None = Depends(require_permission("can_manage_sales_bind_marks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SalesBindMarkResponse]:
    rows = await SalesBindMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=SalesBindMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sales_bind_mark(
    body: SalesBindMarkCreate,
    _authz: None = Depends(require_permission("can_manage_sales_bind_marks", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SalesBindMarkResponse:
    saved = await SalesBindMarkService(session).persist_sales_bind_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bind_kind=body.bind_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
