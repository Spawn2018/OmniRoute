from sqlalchemy import func, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.port import Port

# Postgres dławi się przy jednym INSERT na cały UN/LOCODE (setki tysięcy wierszy).
_UPSERT_BATCH = 1000


class PortRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self, search: str | None = None) -> list[Port]:
        stmt = select(Port).order_by(Port.unlocode)
        token = "" if search is None else search.strip().upper()
        if token != "":
            pattern = f"%{token}%"
            stmt = stmt.where(
                or_(Port.unlocode.like(pattern), func.upper(Port.name).like(pattern)),
            )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def find_by_token(self, *, unlocode: str, alias: str) -> list[Port]:
        stmt = select(Port).where(
            or_(Port.unlocode == unlocode, Port.aliases.contains([alias])),
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def find_by_unlocode(self, unlocode: str) -> Port | None:
        found = await self._session.scalar(select(Port).where(Port.unlocode == unlocode))
        return found if isinstance(found, Port) else None

    async def add(self, row: Port) -> Port:
        self._session.add(row)
        await self._session.flush()
        return row

    async def upsert_many(self, rows: list[dict[str, object]]) -> int:
        upserted = 0
        for start in range(0, len(rows), _UPSERT_BATCH):
            batch = rows[start : start + _UPSERT_BATCH]
            stmt = insert(Port).values(batch)
            stmt = stmt.on_conflict_do_update(
                constraint="uq_port_org_unlocode",
                set_={
                    "name": stmt.excluded.name,
                    "country_code": stmt.excluded.country_code,
                    "lat": stmt.excluded.lat,
                    "lng": stmt.excluded.lng,
                    "is_seaport": stmt.excluded.is_seaport,
                    "function_flags": stmt.excluded.function_flags,
                    "aliases": stmt.excluded.aliases,
                    "source_ref": stmt.excluded.source_ref,
                    "updated_at": func.now(),
                },
            )
            await self._session.execute(stmt)
            upserted += len(batch)
        return upserted
