from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ocean_bill import OceanBill

# D6c: kolejny numer liczy Postgres — wzorzec 619.0 / 72.0, nie pętla w Pythonie.
_ISSUE_HBL_SQL = """
UPDATE ocean_bill AS target
SET bill_no = :prefix || LPAD(nxt.seq::text, 4, '0')
FROM (
    SELECT COALESCE(
        MAX(
            CAST(
                SUBSTRING(bill_no FROM (LENGTH(:prefix) + 1)) AS INTEGER
            )
        ),
        0
    ) + 1 AS seq
    FROM ocean_bill
    WHERE bill_no IS NOT NULL
      AND bill_kind = 'hbl'
      AND LENGTH(bill_no) = LENGTH(:prefix) + 4
      AND bill_no LIKE :prefix || '%'
) AS nxt
WHERE target.id = :bid
  AND target.bill_kind = 'hbl'
  AND target.bill_no IS NULL
RETURNING target.id, target.bill_no, target.bill_kind
"""

_ISSUE_MBL_SQL = """
UPDATE ocean_bill AS target
SET bill_no = :prefix || LPAD(nxt.seq::text, 4, '0')
FROM (
    SELECT COALESCE(
        MAX(
            CAST(
                SUBSTRING(bill_no FROM (LENGTH(:prefix) + 1)) AS INTEGER
            )
        ),
        0
    ) + 1 AS seq
    FROM ocean_bill
    WHERE bill_no IS NOT NULL
      AND bill_kind = 'mbl'
      AND LENGTH(bill_no) = LENGTH(:prefix) + 4
      AND bill_no LIKE :prefix || '%'
) AS nxt
WHERE target.id = :bid
  AND target.bill_kind = 'mbl'
  AND target.bill_no IS NULL
RETURNING target.id, target.bill_no, target.bill_kind
"""


class OceanBillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[OceanBill]:
        result = await self._session.scalars(
            select(OceanBill).order_by(
                OceanBill.created_at.desc(),
                OceanBill.id,
            ),
        )
        return list(result.all())

    async def get(self, bill_id: UUID) -> OceanBill | None:
        found = await self._session.get(OceanBill, bill_id)
        return found if isinstance(found, OceanBill) else None

    async def add(self, row: OceanBill) -> OceanBill:
        self._session.add(row)
        await self._session.flush()
        return row

    async def issue_hbl(self, *, bill_id: UUID, prefix: str) -> OceanBill | None:
        result = await self._session.execute(
            text(_ISSUE_HBL_SQL),
            {"bid": bill_id, "prefix": prefix},
        )
        row = result.mappings().first()
        if row is None:
            return None
        cached = await self._session.get(OceanBill, bill_id)
        if cached is None:
            return None
        await self._session.refresh(cached)
        return cached

    async def issue_mbl(self, *, bill_id: UUID, prefix: str) -> OceanBill | None:
        result = await self._session.execute(
            text(_ISSUE_MBL_SQL),
            {"bid": bill_id, "prefix": prefix},
        )
        row = result.mappings().first()
        if row is None:
            return None
        cached = await self._session.get(OceanBill, bill_id)
        if cached is None:
            return None
        await self._session.refresh(cached)
        return cached
