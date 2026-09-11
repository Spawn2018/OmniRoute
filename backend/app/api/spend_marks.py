from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.spend_mark import SpendMark
from app.services.spend_marks.spend_mark_service import SpendMarkService

router = APIRouter(prefix="/spend-marks", tags=["spend-marks"])

_PERM = "can_manage_spend_marks"


class SpendMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    leakage_kind: str
    source_ref: str


class SpendMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    leakage_kind: str
    source_ref: str


def _mark(saved: SpendMark) -> SpendMarkResponse:
    return SpendMarkResponse.model_validate(saved)


@router.get("", response_model=list[SpendMarkResponse])
async def list_spend_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SpendMarkResponse]:
    packed = await SpendMarkService(session).list_marks()
    return [_mark(item) for item in packed]


@router.post(
    "",
    response_model=SpendMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_spend_mark(
    body: SpendMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SpendMarkResponse:
    saved = await SpendMarkService(session).persist_spend_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        leakage_kind=body.leakage_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _mark(saved)
