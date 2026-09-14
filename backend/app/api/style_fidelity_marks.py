from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.style_fidelity_mark import StyleFidelityMark
from app.services.style_fidelity_marks.style_fidelity_mark_service import (
    StyleFidelityMarkService,
)

router = APIRouter(
    prefix="/style-fidelity-marks",
    tags=["style-fidelity-marks"],
)

_PERM = "can_manage_style_fidelity_marks"


class StyleFidelityMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    fidelity_kind: str
    source_ref: str


class StyleFidelityMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    fidelity_kind: str
    source_ref: str


def _row(saved: StyleFidelityMark) -> StyleFidelityMarkResponse:
    return StyleFidelityMarkResponse.model_validate(saved)


@router.get("", response_model=list[StyleFidelityMarkResponse])
async def list_style_fidelity_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[StyleFidelityMarkResponse]:
    packed = await StyleFidelityMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=StyleFidelityMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_style_fidelity_mark(
    body: StyleFidelityMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> StyleFidelityMarkResponse:
    saved = await StyleFidelityMarkService(session).persist_style_fidelity_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        fidelity_kind=body.fidelity_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
