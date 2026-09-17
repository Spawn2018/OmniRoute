from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.self_billing_mark import SelfBillingMark
from app.services.self_billing_marks.self_billing_mark_service import SelfBillingMarkService

router = APIRouter(prefix="/self-billing-marks", tags=["self-billing-marks"])

_PERM = "can_manage_self_billing_marks"


class SelfBillingMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    billing_kind: str
    source_ref: str


class SelfBillingMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    billing_kind: str
    source_ref: str


def _row(saved: SelfBillingMark) -> SelfBillingMarkResponse:
    return SelfBillingMarkResponse.model_validate(saved)


@router.get("", response_model=list[SelfBillingMarkResponse])
async def list_self_billing_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SelfBillingMarkResponse]:
    packed = await SelfBillingMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=SelfBillingMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_self_billing_mark(
    body: SelfBillingMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SelfBillingMarkResponse:
    saved = await SelfBillingMarkService(session).persist_self_billing_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        billing_kind=body.billing_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
