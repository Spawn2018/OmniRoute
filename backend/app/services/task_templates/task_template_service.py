from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.task_template import (
    require_task_applies_when,
    require_task_template_code,
    require_task_template_source_ref,
)
from app.models.task_template import TaskTemplate
from app.repositories.task_templates.task_template_repository import TaskTemplateRepository


class TaskTemplateService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TaskTemplateRepository(session)

    async def list_templates(self) -> list[TaskTemplate]:
        return await self._rows.fetch_templates()

    async def record_template(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        template_code: object,
        applies_when: object,
        source_ref: object,
    ) -> TaskTemplate:
        code = require_task_template_code(template_code)
        when = require_task_applies_when(applies_when)
        origin = require_task_template_source_ref(source_ref)
        packed = TaskTemplate(
            id=uuid4(),
            organization_id=organization_id,
            template_code=code,
            applies_when=when,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add(packed)
