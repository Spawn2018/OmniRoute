from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.handover_note import HandoverNote


class HandoverNoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_notes(self) -> list[HandoverNote]:
        stmt = select(HandoverNote).order_by(
            HandoverNote.note_code,
            HandoverNote.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_note(self, row: HandoverNote) -> HandoverNote:
        self._session.add(row)
        await self._session.flush()
        return row
