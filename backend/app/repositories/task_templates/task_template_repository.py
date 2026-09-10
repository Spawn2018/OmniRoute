from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_template import TaskTemplate


class TaskTemplateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def fetch_templates(self) -> list[TaskTemplate]:
        stmt = select(TaskTemplate).order_by(TaskTemplate.template_code, TaskTemplate.id)
        executed = await self._db.execute(stmt)
        return list(executed.scalars())

    async def add(self, row: TaskTemplate) -> TaskTemplate:
        self._db.add(row)
        await self._db.flush()
        return row
