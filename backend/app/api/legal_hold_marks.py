from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.legal_hold_mark import LegalHoldMark
from app.services.legal_hold_marks.legal_hold_mark_service import LegalHoldMarkService

router = APIRouter(prefix="/legal-hold-marks", tags=["legal-hold-marks"])

_PERM = "can_manage_legal_hold_marks"


class LegalHoldMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    hold_kind: str
    source_ref: str


class LegalHoldMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    hold_kind: str
    source_ref: str


def _row(saved: LegalHoldMark) -> LegalHoldMarkResponse:
    return LegalHoldMarkResponse.model_validate(saved)


@router.get("", response_model=list[LegalHoldMarkResponse])
async def list_legal_hold_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LegalHoldMarkResponse]:
    packed = await LegalHoldMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=LegalHoldMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_legal_hold_mark(
    body: LegalHoldMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LegalHoldMarkResponse:
    saved = await LegalHoldMarkService(session).persist_legal_hold_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        hold_kind=body.hold_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
