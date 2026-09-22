from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment_leg import ShipmentLeg

# U3c: kolejny numer liczy Postgres — wzorzec 72.0, nie pętla w Pythonie.
_ISSUE_HAWB_SQL = """
UPDATE shipment_leg AS target
SET hawb_no = :prefix || LPAD(nxt.seq::text, 4, '0')
FROM (
    SELECT COALESCE(
        MAX(
            CAST(
                SUBSTRING(hawb_no FROM (LENGTH(:prefix) + 1)) AS INTEGER
            )
        ),
        0
    ) + 1 AS seq
    FROM shipment_leg
    WHERE hawb_no IS NOT NULL
      AND LENGTH(hawb_no) = LENGTH(:prefix) + 4
      AND hawb_no LIKE :prefix || '%'
) AS nxt
WHERE target.id = :lid
  AND target.leg_kind = 'air'
  AND target.hawb_no IS NULL
RETURNING target.id, target.hawb_no, target.mawb_no
"""

_ISSUE_MAWB_SQL = """
UPDATE shipment_leg AS target
SET mawb_no = :prefix || LPAD(nxt.seq::text, 4, '0')
FROM (
    SELECT COALESCE(
        MAX(
            CAST(
                SUBSTRING(mawb_no FROM (LENGTH(:prefix) + 1)) AS INTEGER
            )
        ),
        0
    ) + 1 AS seq
    FROM shipment_leg
    WHERE mawb_no IS NOT NULL
      AND LENGTH(mawb_no) = LENGTH(:prefix) + 4
      AND mawb_no LIKE :prefix || '%'
) AS nxt
WHERE target.id = :lid
  AND target.leg_kind = 'air'
  AND target.mawb_no IS NULL
RETURNING target.id, target.hawb_no, target.mawb_no
"""


class ShipmentLegRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[ShipmentLeg]:
        result = await self._session.scalars(
            select(ShipmentLeg).order_by(ShipmentLeg.created_at.desc()),
        )
        return list(result.all())

    async def get(self, leg_id: UUID) -> ShipmentLeg | None:
        found = await self._session.get(ShipmentLeg, leg_id)
        return found if isinstance(found, ShipmentLeg) else None

    async def add(self, row: ShipmentLeg) -> ShipmentLeg:
        self._session.add(row)
        await self._session.flush()
        return row

    async def issue_hawb(self, *, leg_id: UUID, prefix: str) -> ShipmentLeg | None:
        result = await self._session.execute(
            text(_ISSUE_HAWB_SQL),
            {"lid": leg_id, "prefix": prefix},
        )
        row = result.mappings().first()
        if row is None:
            return None
        cached = await self._session.get(ShipmentLeg, leg_id)
        if cached is None:
            return None
        await self._session.refresh(cached)
        return cached

    async def issue_mawb(self, *, leg_id: UUID, prefix: str) -> ShipmentLeg | None:
        result = await self._session.execute(
            text(_ISSUE_MAWB_SQL),
            {"lid": leg_id, "prefix": prefix},
        )
        row = result.mappings().first()
        if row is None:
            return None
        cached = await self._session.get(ShipmentLeg, leg_id)
        if cached is None:
            return None
        await self._session.refresh(cached)
        return cached
