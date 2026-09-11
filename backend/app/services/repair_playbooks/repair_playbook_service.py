from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repair_playbook import parse_repair_playbook_row
from app.models.repair_playbook import RepairPlaybook
from app.repositories.repair_playbooks.repair_playbook_repository import (
    RepairPlaybookRepository,
)


class RepairPlaybookService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RepairPlaybookRepository(session)

    async def list_playbooks(self) -> list[RepairPlaybook]:
        return await self._rows.list_playbooks()

    async def persist_repair_playbook(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        playbook_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> RepairPlaybook:
        code, stance, origin = parse_repair_playbook_row(
            playbook_code, stance_kind, source_ref
        )
        row = RepairPlaybook(
            id=uuid4(),
            organization_id=organization_id,
            playbook_code=code,
            stance_kind=stance,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_playbook(row)
