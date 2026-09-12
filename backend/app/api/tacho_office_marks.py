"""HTTP katalog reefer — HITL, bez live filing."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tacho_office_mark import TachoOfficeMark
from app.services.tacho_office_marks.tacho_office_mark_service import TachoOfficeMarkService

router = APIRouter(prefix="/tacho-office-marks", tags=["empty-depot"])

_PERM = "can_manage_tacho_office_marks"


class TachoOfficeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    tacho_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class TachoOfficeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    tacho_kind: str
    source_ref: str


def _to_dto(row: TachoOfficeMark) -> TachoOfficeMarkResponse:
    return TachoOfficeMarkResponse.model_validate(row)


@router.get("", response_model=list[TachoOfficeMarkResponse])
async def list_tacho_office_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TachoOfficeMarkResponse]:
    catalog = TachoOfficeMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=TachoOfficeMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_tacho_office_mark(
    body: TachoOfficeMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TachoOfficeMarkResponse:
    catalog = TachoOfficeMarkService(session)
    saved = await catalog.persist_tacho_office_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        tacho_kind=body.tacho_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "tacho-office-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
