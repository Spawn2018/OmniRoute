from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.billing_mark import BillingMark
from app.services.billing_marks.billing_mark_service import BillingMarkService

router = APIRouter(prefix="/billing-marks", tags=["billing-marks"])

_PERM = "can_manage_billing_marks"


class BillingMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    billing_kind: str
    source_ref: str


class BillingMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    billing_kind: str
    source_ref: str


def _row(saved: BillingMark) -> BillingMarkResponse:
    return BillingMarkResponse.model_validate(saved)


@router.get("", response_model=list[BillingMarkResponse])
async def list_billing_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BillingMarkResponse]:
    packed = await BillingMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=BillingMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_billing_mark(
    body: BillingMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BillingMarkResponse:
    saved = await BillingMarkService(session).persist_billing_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        billing_kind=body.billing_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
