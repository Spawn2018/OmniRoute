"""Seed lokalny: organization + app_user z hasłem + OpenFGA member.

Wymaga: Postgres (migracje), OpenFGA na OPENFGA_API_URL (domyślnie :8080).
Wypisuje email/hasło do UI /session oraz wartości do .env.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.core.database import bind_tenant  # noqa: E402
from app.core.password_hash import hash_password  # noqa: E402
from app.integrations.openfga.client import (  # noqa: E402
    OpenFgaAuthz,
    bootstrap_store,
    build_openfga_client,
)
from app.models.app_user import AppUser  # noqa: E402
from app.models.organization import Organization  # noqa: E402


async def main() -> None:
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://omniroute:omniroute@127.0.0.1:5432/omniroute",
    )
    openfga_url = os.getenv("OPENFGA_API_URL", "http://127.0.0.1:8080")

    org_id = uuid4()
    user_id = uuid4()

    engine = create_async_engine(database_url, pool_pre_ping=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with session_factory() as session:
        await bind_tenant(session, org_id)
        session.add(
            Organization(
                id=org_id,
                name="Dev Local",
                slug=f"dev-local-{org_id.hex[:8]}",
                created_by=user_id,
            ),
        )
        await session.flush()
        session.add(
            AppUser(
                id=user_id,
                organization_id=org_id,
                email="dev@local.test",
                display_name="Dev Local",
                password_hash=hash_password("correct-horse-battery"),
                created_by=user_id,
            ),
        )
        await session.commit()

    await engine.dispose()

    os.environ["OPENFGA_API_URL"] = openfga_url
    from app.core import config as config_module

    config_module.settings.openfga_api_url = openfga_url
    config_module.settings.openfga_store_id = ""
    config_module.settings.openfga_model_id = ""

    client = await build_openfga_client()
    try:
        store_id, model_id = await bootstrap_store(client, store_name=f"local-{org_id.hex[:8]}")
        authz = OpenFgaAuthz(client)
        await authz.write_member(user_id=user_id, organization_id=org_id)
    finally:
        await client.close()

    print()
    print("SEED OK — logowanie /session:")
    print("  email    = dev@local.test")
    print("  password = correct-horse-battery")
    print()
    print("Ustaw w środowisku API (PowerShell):")
    print('  $env:OPENFGA_API_URL="http://127.0.0.1:8080"')
    print(f'  $env:OPENFGA_STORE_ID="{store_id}"')
    print(f'  $env:OPENFGA_MODEL_ID="{model_id}"')
    print('  $env:JWT_SECRET="change-me-local-only-not-for-production"')
    print()
    print("Albo dopisz do .env i zrestartuj API.")


if __name__ == "__main__":
    asyncio.run(main())
