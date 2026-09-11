from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.what_if_mark import parse_what_if_mark_row
from app.models.what_if_mark import WhatIfMark
from app.repositories.what_if_marks.what_if_mark_repository import (
    WhatIfMarkRepository,
)


class WhatIfMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = WhatIfMarkRepository(session)

    async def list_marks(self) -> list[WhatIfMark]:
        return await self._rows.list_marks()

    async def persist_what_if_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        scenario_kind: object,
        source_ref: object,
    ) -> WhatIfMark:
        code, kind, origin = parse_what_if_mark_row(
            mark_code,
            scenario_kind,
            source_ref,
        )
        row = WhatIfMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            scenario_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
