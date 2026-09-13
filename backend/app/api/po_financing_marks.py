from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.po_financing_mark import PoFinancingMark
from app.services.po_financing_marks.po_financing_mark_service import PoFinancingMarkService

router = APIRouter(prefix="/po-financing-marks", tags=["po-financing-marks"])

_PERM = "can_manage_po_financing_marks"


class PoFinancingMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    financing_kind: str
    source_ref: str


class PoFinancingMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    financing_kind: str
    source_ref: str


def _row(saved: PoFinancingMark) -> PoFinancingMarkResponse:
    return PoFinancingMarkResponse.model_validate(saved)


@router.get("", response_model=list[PoFinancingMarkResponse])
async def list_po_financing_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PoFinancingMarkResponse]:
    packed = await PoFinancingMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PoFinancingMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_po_financing_mark(
    body: PoFinancingMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PoFinancingMarkResponse:
    saved = await PoFinancingMarkService(session).persist_po_financing_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        financing_kind=body.financing_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
