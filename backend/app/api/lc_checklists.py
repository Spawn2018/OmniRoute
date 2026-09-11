from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.lc_checklist import LcChecklist
from app.services.lc_checklists.lc_checklist_service import LcChecklistService

router = APIRouter(prefix="/lc-checklists", tags=["lc-checklists"])

_PERM = "can_manage_lc_checklists"


class LcChecklistCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    checklist_code: str
    status_kind: str
    source_ref: str


class LcChecklistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    checklist_code: str
    status_kind: str
    source_ref: str


def _row(saved: LcChecklist) -> LcChecklistResponse:
    return LcChecklistResponse.model_validate(saved)


@router.get("", response_model=list[LcChecklistResponse])
async def list_lc_checklists(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LcChecklistResponse]:
    packed = await LcChecklistService(session).list_checklists()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=LcChecklistResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lc_checklist(
    body: LcChecklistCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LcChecklistResponse:
    saved = await LcChecklistService(session).persist_lc_checklist(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        checklist_code=body.checklist_code,
        status_kind=body.status_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
