from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ncts_draft import NctsDraft
from app.services.ncts_drafts.ncts_draft_service import NctsDraftService

router = APIRouter(prefix="/ncts-drafts", tags=["ncts-drafts"])

_PERM = "can_manage_ncts_drafts"


class NctsDraftCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    draft_code: str
    transit_kind: str
    source_ref: str


class NctsDraftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    draft_code: str
    transit_kind: str
    source_ref: str


def _row(saved: NctsDraft) -> NctsDraftResponse:
    return NctsDraftResponse.model_validate(saved)


@router.get("", response_model=list[NctsDraftResponse])
async def list_ncts_drafts(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NctsDraftResponse]:
    packed = await NctsDraftService(session).list_drafts()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=NctsDraftResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ncts_draft(
    body: NctsDraftCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NctsDraftResponse:
    saved = await NctsDraftService(session).persist_ncts_draft(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        draft_code=body.draft_code,
        transit_kind=body.transit_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
