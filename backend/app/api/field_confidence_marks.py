from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.field_confidence_mark import FieldConfidenceMark
from app.services.field_confidence_marks.field_confidence_mark_service import (
    FieldConfidenceMarkService,
)

router = APIRouter(
    prefix="/field-confidence-marks",
    tags=["field-confidence-marks"],
)

_PERM = "can_manage_field_confidence_marks"


class FieldConfidenceMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    band_kind: str
    source_ref: str


class FieldConfidenceMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    band_kind: str
    source_ref: str


def _row(saved: FieldConfidenceMark) -> FieldConfidenceMarkResponse:
    return FieldConfidenceMarkResponse.model_validate(saved)


@router.get("", response_model=list[FieldConfidenceMarkResponse])
async def list_field_confidence_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FieldConfidenceMarkResponse]:
    packed = await FieldConfidenceMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=FieldConfidenceMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_field_confidence_mark(
    body: FieldConfidenceMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FieldConfidenceMarkResponse:
    saved = await FieldConfidenceMarkService(session).persist_field_confidence_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        band_kind=body.band_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
