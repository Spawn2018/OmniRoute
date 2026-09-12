from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.general_average_mark import GeneralAverageMark
from app.services.general_average_marks.general_average_mark_service import (
    GeneralAverageMarkService,
)

router = APIRouter(prefix="/general-average-marks", tags=["general-average-marks"])

_PERM = "can_manage_general_average_marks"


class GeneralAverageMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    average_kind: str
    source_ref: str


class GeneralAverageMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    average_kind: str
    source_ref: str


def _row(saved: GeneralAverageMark) -> GeneralAverageMarkResponse:
    return GeneralAverageMarkResponse.model_validate(saved)


@router.get("", response_model=list[GeneralAverageMarkResponse])
async def list_general_average_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[GeneralAverageMarkResponse]:
    packed = await GeneralAverageMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=GeneralAverageMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_general_average_mark(
    body: GeneralAverageMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> GeneralAverageMarkResponse:
    saved = await GeneralAverageMarkService(session).persist_general_average_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        average_kind=body.average_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
