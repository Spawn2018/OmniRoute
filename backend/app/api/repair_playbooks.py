from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.repair_playbook import RepairPlaybook
from app.services.repair_playbooks.repair_playbook_service import (
    RepairPlaybookService,
)

router = APIRouter(prefix="/repair-playbooks", tags=["repair-playbooks"])

_PERM = "can_manage_repair_playbooks"


class RepairPlaybookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    playbook_code: str
    stance_kind: str
    source_ref: str


class RepairPlaybookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    playbook_code: str
    stance_kind: str
    source_ref: str


def _playbook(saved: RepairPlaybook) -> RepairPlaybookResponse:
    return RepairPlaybookResponse.model_validate(saved)


@router.get("", response_model=list[RepairPlaybookResponse])
async def list_repair_playbooks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RepairPlaybookResponse]:
    packed = await RepairPlaybookService(session).list_playbooks()
    return [_playbook(item) for item in packed]


@router.post(
    "",
    response_model=RepairPlaybookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_repair_playbook(
    body: RepairPlaybookCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RepairPlaybookResponse:
    saved = await RepairPlaybookService(session).persist_repair_playbook(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        playbook_code=body.playbook_code,
        stance_kind=body.stance_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _playbook(saved)
