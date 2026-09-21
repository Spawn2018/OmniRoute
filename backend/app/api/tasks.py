from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.task import Task
from app.services.tasks.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

_PERM = "can_manage_tasks"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_code: str
    template_code: str
    status_kind: str
    source_ref: str


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    task_code: str
    template_code: str
    status_kind: str
    source_ref: str


def _row(saved: Task) -> TaskResponse:
    return TaskResponse.model_validate(saved)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TaskResponse]:
    packed = await TaskService(session).list_tasks()
    return [_row(item) for item in packed]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TaskResponse:
    saved = await TaskService(session).persist_task(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        task_code=body.task_code,
        template_code=body.template_code,
        status_kind=body.status_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
