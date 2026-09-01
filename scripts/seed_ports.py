"""Ingest UN/LOCODE do katalogu port jednego tenanta.

Jedyne miejsce, które sięga po zewnętrzne źródło. Endpoint /ports nigdy tego nie robi.
Źródło: https://github.com/cristan/improved-un-locodes — podaj plik i pin rewizji.

    python scripts/seed_ports.py --organization <uuid> --file code-list.json --pin <sha>
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
from app.services.geography.unlocode_ingest import (  # noqa: E402
    ingest_ports,
    parse_unlocode_records,
)

_SOURCE = "github:cristan/improved-un-locodes"


async def seed(organization_id: UUID, payload: str, pin: str) -> int:
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://omniroute:omniroute@127.0.0.1:5432/omniroute",
    )
    records = parse_unlocode_records(payload)

    engine = create_async_engine(database_url, pool_pre_ping=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with session_factory() as session:
        await bind_tenant(session, organization_id)
        upserted = await ingest_ports(
            session,
            organization_id=organization_id,
            records=records,
            source_ref=f"{_SOURCE}@{pin}",
        )
        await session.commit()
    await engine.dispose()
    return upserted


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest UN/LOCODE dla tenanta")
    parser.add_argument("--organization", required=True, type=UUID)
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--pin", required=True, help="SHA rewizji źródła w source_ref")
    args = parser.parse_args()

    payload = args.file.read_text(encoding="utf-8")
    upserted = asyncio.run(seed(args.organization, payload, args.pin))
    print(f"port: {upserted} wierszy dla {args.organization}")


if __name__ == "__main__":
    main()
