from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mail_accept_mark import MailAcceptMark


def _label_parking_catalog_query() -> Select[tuple[MailAcceptMark]]:
    return select(MailAcceptMark).order_by(
        MailAcceptMark.mark_code.asc(),
        MailAcceptMark.created_at.desc(),
    )

class MailAcceptMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[MailAcceptMark]:
        loaded = await self._session.scalars(_label_parking_catalog_query())
        batch: Sequence[MailAcceptMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: MailAcceptMark) -> MailAcceptMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
