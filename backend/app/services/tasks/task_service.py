from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.task import parse_task_row
from app.models.task import Task
from app.repositories.tasks.task_repository import TaskRepository


class TaskService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TaskRepository(session)

    async def list_tasks(self) -> list[Task]:
        return await self._rows.list_tasks()

    async def persist_task(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        task_code: object,
        template_code: object,
        status_kind: object,
        source_ref: object,
    ) -> Task:
        code, template, status, origin = parse_task_row(
            task_code,
            template_code,
            status_kind,
            source_ref,
        )
        row = Task(
            id=uuid4(),
            organization_id=organization_id,
            task_code=code,
            template_code=template,
            status_kind=status,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_task(row)
