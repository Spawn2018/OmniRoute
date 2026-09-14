from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.quality_descent_mark import QualityDescentMark
from app.services.quality_descent_marks.quality_descent_mark_service import (
    QualityDescentMarkService,
)

router = APIRouter(
    prefix="/quality-descent-marks",
    tags=["quality-descent-marks"],
)

_PERM = "can_manage_quality_descent_marks"


class QualityDescentMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    descent_kind: str
    source_ref: str


class QualityDescentMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    descent_kind: str
    source_ref: str


def _row(saved: QualityDescentMark) -> QualityDescentMarkResponse:
    return QualityDescentMarkResponse.model_validate(saved)


@router.get("", response_model=list[QualityDescentMarkResponse])
async def list_quality_descent_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[QualityDescentMarkResponse]:
    packed = await QualityDescentMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=QualityDescentMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_quality_descent_mark(
    body: QualityDescentMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> QualityDescentMarkResponse:
    saved = await QualityDescentMarkService(session).persist_quality_descent_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        descent_kind=body.descent_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
