from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.what_if_mark import WhatIfMark


class WhatIfMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[WhatIfMark]:
        packed = await self._session.scalars(
            select(WhatIfMark).order_by(
                WhatIfMark.mark_code,
                WhatIfMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: WhatIfMark) -> WhatIfMark:
        self._session.add(row)
        await self._session.flush()
        return row
