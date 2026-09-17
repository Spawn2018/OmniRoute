from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.handover_note import HandoverNote
from app.services.handover_notes.handover_note_service import HandoverNoteService

router = APIRouter(
    prefix="/handover-notes",
    tags=["handover-notes"],
)

_PERM = "can_manage_handover_notes"


class HandoverNoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note_code: str
    situation: str
    background: str
    assessment: str
    recommendation: str
    source_ref: str


class HandoverNoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    note_code: str
    situation: str
    background: str
    assessment: str
    recommendation: str
    source_ref: str


def _row(saved: HandoverNote) -> HandoverNoteResponse:
    return HandoverNoteResponse.model_validate(saved)


@router.get("", response_model=list[HandoverNoteResponse])
async def list_handover_notes(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[HandoverNoteResponse]:
    packed = await HandoverNoteService(session).list_notes()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=HandoverNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_handover_note(
    body: HandoverNoteCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> HandoverNoteResponse:
    saved = await HandoverNoteService(session).persist_handover_note(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        note_code=body.note_code,
        situation=body.situation,
        background=body.background,
        assessment=body.assessment,
        recommendation=body.recommendation,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
