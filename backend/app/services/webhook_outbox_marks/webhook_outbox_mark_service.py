from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.webhook_outbox_mark import parse_webhook_outbox_mark_row
from app.models.webhook_outbox_mark import WebhookOutboxMark
from app.repositories.webhook_outbox_marks.webhook_outbox_mark_repository import (
    WebhookOutboxMarkRepository,
)


class WebhookOutboxMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = WebhookOutboxMarkRepository(session)

    async def list_marks(self) -> list[WebhookOutboxMark]:
        return await self._rows.list_marks()

    async def persist_webhook_outbox_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        outbox_kind: object,
        source_ref: object,
    ) -> WebhookOutboxMark:
        code, kind, origin = parse_webhook_outbox_mark_row(
            mark_code,
            outbox_kind,
            source_ref,
        )
        row = WebhookOutboxMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            outbox_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
