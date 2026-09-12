from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.eur1_atr_mark import Eur1AtrMark
from app.services.eur1_atr_marks.eur1_atr_mark_service import (
    Eur1AtrMarkService,
)

router = APIRouter(prefix="/eur1-atr-marks", tags=["eur1-atr-marks"])

_PERM = "can_manage_eur1_atr_marks"


class Eur1AtrMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    cert_kind: str
    source_ref: str


class Eur1AtrMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    cert_kind: str
    source_ref: str


def _row(saved: Eur1AtrMark) -> Eur1AtrMarkResponse:
    return Eur1AtrMarkResponse.model_validate(saved)


@router.get("", response_model=list[Eur1AtrMarkResponse])
async def list_eur1_atr_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[Eur1AtrMarkResponse]:
    packed = await Eur1AtrMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=Eur1AtrMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_eur1_atr_mark(
    body: Eur1AtrMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> Eur1AtrMarkResponse:
    saved = await Eur1AtrMarkService(session).persist_eur1_atr_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        cert_kind=body.cert_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
