from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repair_playbook import RepairPlaybook


class RepairPlaybookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_playbooks(self) -> list[RepairPlaybook]:
        packed = await self._session.scalars(
            select(RepairPlaybook).order_by(
                RepairPlaybook.playbook_code,
                RepairPlaybook.id,
            ),
        )
        return list(packed.all())

    async def add_playbook(self, row: RepairPlaybook) -> RepairPlaybook:
        self._session.add(row)
        await self._session.flush()
        return row
