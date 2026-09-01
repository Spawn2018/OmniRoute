"""Ingest World Port Index (NGA Pub 150) na istniejące porty tenanta.

Jedyne miejsce, które sięga po zewnętrzne źródło WPI. Endpoint /ports i
/terminals nigdy tego nie robią. UPDATE po zwiniętym UN/LOCODE — nie tworzy portu.

    python scripts/seed_wpi.py --organization <uuid> --file UpdatedPub150.csv --pin <sha>
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.core.database import bind_tenant  # noqa: E402
from app.services.geography.wpi_ingest import ingest_wpi, parse_wpi_records  # noqa: E402

_SOURCE = "nga:pub150"


async def seed(organization_id: UUID, payload: str, pin: str) -> int:
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://omniroute:omniroute@127.0.0.1:5432/omniroute",
    )
    records = parse_wpi_records(payload)

    engine = create_async_engine(database_url, pool_pre_ping=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with session_factory() as session:
        await bind_tenant(session, organization_id)
        updated = await ingest_wpi(
            session,
            organization_id=organization_id,
            records=records,
            source_ref=f"{_SOURCE}@{pin}",
        )
        await session.commit()
    await engine.dispose()
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest World Port Index dla tenanta")
    parser.add_argument("--organization", required=True, type=UUID)
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--pin", required=True, help="SHA pliku źródła w wpi_source_ref")
    args = parser.parse_args()

    payload = args.file.read_text(encoding="utf-8")
    updated = asyncio.run(seed(args.organization, payload, args.pin))
    print(f"wpi: {updated} portów zaktualizowanych dla {args.organization}")


if __name__ == "__main__":
    main()
