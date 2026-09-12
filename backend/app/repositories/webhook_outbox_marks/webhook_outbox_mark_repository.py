from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook_outbox_mark import WebhookOutboxMark


class WebhookOutboxMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[WebhookOutboxMark]:
        packed = await self._session.scalars(
            select(WebhookOutboxMark).order_by(
                WebhookOutboxMark.mark_code,
                WebhookOutboxMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: WebhookOutboxMark) -> WebhookOutboxMark:
        self._session.add(row)
        await self._session.flush()
        return row
