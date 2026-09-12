"""HTTP katalog stance slotu — HITL, bez live T8 i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.slot_guarantee_mark import SlotGuaranteeMark
from app.services.slot_guarantee_marks.slot_guarantee_mark_service import (
    SlotGuaranteeMarkService,
)

router = APIRouter(prefix="/slot-guarantee-marks", tags=["slot-guarantee-mark"])
_PERM = "can_manage_slot_guarantee_marks"


class SlotGuaranteeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    stance_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class SlotGuaranteeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    stance_kind: str
    source_ref: str


def _to_dto(row: SlotGuaranteeMark) -> SlotGuaranteeMarkResponse:
    return SlotGuaranteeMarkResponse.model_validate(row)


@router.get("", response_model=list[SlotGuaranteeMarkResponse])
async def list_slot_guarantee_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SlotGuaranteeMarkResponse]:
    catalog = SlotGuaranteeMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=SlotGuaranteeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_slot_guarantee_mark(
    body: SlotGuaranteeMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SlotGuaranteeMarkResponse:
    catalog = SlotGuaranteeMarkService(session)
    saved = await catalog.persist_slot_guarantee_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        stance_kind=body.stance_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "slot-guarantee-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
