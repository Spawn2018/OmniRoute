from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_tasks(self) -> list[Task]:
        stmt = select(Task).order_by(Task.task_code, Task.id)
        return list((await self._session.scalars(stmt)).all())

    async def add_task(self, row: Task) -> Task:
        self._session.add(row)
        await self._session.flush()
        return row
