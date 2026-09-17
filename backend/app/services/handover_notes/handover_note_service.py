from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.handover_note import parse_handover_note_row
from app.models.handover_note import HandoverNote
from app.repositories.handover_notes.handover_note_repository import (
    HandoverNoteRepository,
)


class HandoverNoteService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = HandoverNoteRepository(session)

    async def list_notes(self) -> list[HandoverNote]:
        return await self._rows.list_notes()

    async def persist_handover_note(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        note_code: object,
        situation: object,
        background: object,
        assessment: object,
        recommendation: object,
        source_ref: object,
    ) -> HandoverNote:
        code, sit, back, assess, rec, origin = parse_handover_note_row(
            note_code,
            situation,
            background,
            assessment,
            recommendation,
            source_ref,
        )
        row = HandoverNote(
            id=uuid4(),
            organization_id=organization_id,
            note_code=code,
            situation=sit,
            background=back,
            assessment=assess,
            recommendation=rec,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_note(row)
