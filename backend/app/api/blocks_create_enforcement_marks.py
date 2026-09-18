from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.blocks_create_enforcement_mark import BlocksCreateEnforcementMark
from app.services.blocks_create_enforcement_marks.blocks_create_enforcement_mark_service import (
    BlocksCreateEnforcementMarkService,
)

router = APIRouter(
    prefix="/blocks-create-enforcement-marks",
    tags=["blocks-create-enforcement-marks"],
)

_PERM = "can_manage_blocks_create_enforcement_marks"


class BlocksCreateEnforcementMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    enforcement_kind: str
    source_ref: str


class BlocksCreateEnforcementMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    enforcement_kind: str
    source_ref: str


def _row(saved: BlocksCreateEnforcementMark) -> BlocksCreateEnforcementMarkResponse:
    return BlocksCreateEnforcementMarkResponse.model_validate(saved)


@router.get("", response_model=list[BlocksCreateEnforcementMarkResponse])
async def list_blocks_create_enforcement_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BlocksCreateEnforcementMarkResponse]:
    packed = await BlocksCreateEnforcementMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=BlocksCreateEnforcementMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_blocks_create_enforcement_mark(
    body: BlocksCreateEnforcementMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BlocksCreateEnforcementMarkResponse:
    saved = await BlocksCreateEnforcementMarkService(
        session,
    ).persist_blocks_create_enforcement_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        enforcement_kind=body.enforcement_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
