from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.task_template import TaskTemplate
from app.services.outbox_events.outbox_event_service import OutboxEventService
from app.services.task_templates.task_template_service import TaskTemplateService

router = APIRouter(prefix="/task-templates", tags=["task-templates"])

_PERM = "can_manage_task_templates"


class TaskTemplateCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template_code: str
    applies_when: str
    source_ref: str


class TaskTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    template_code: str
    applies_when: str
    source_ref: str


def _as_row(row: TaskTemplate) -> TaskTemplateResponse:
    return TaskTemplateResponse.model_validate(row)


@router.get("", response_model=list[TaskTemplateResponse])
async def list_task_templates(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TaskTemplateResponse]:
    rows = await TaskTemplateService(session).list_templates()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TaskTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_task_template(
    body: TaskTemplateCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TaskTemplateResponse:
    row = await TaskTemplateService(session).record_template(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        template_code=body.template_code,
        applies_when=body.applies_when,
        source_ref=body.source_ref,
    )
    await OutboxEventService(session).record_template_saved(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_id=row.id,
        source_ref=f"outbox://task-template/{row.id}",
    )
    await session.commit()
    return _as_row(row)
