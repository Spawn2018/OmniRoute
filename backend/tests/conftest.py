import os
import uuid
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from alembic import command
from app.core.database import bind_tenant
from app.models.app_user import AppUser
from app.models.carrier_inquiry import CarrierInquiry  # noqa: F401 — rejestr metadanych RLS
from app.models.carrier_profile import CarrierProfile  # noqa: F401 — rejestr metadanych RLS
from app.models.channel_quote import ChannelQuote  # noqa: F401 — rejestr metadanych RLS
from app.models.charge import Charge  # noqa: F401 — rejestr metadanych RLS
from app.models.charge_code import ChargeCode  # noqa: F401 — rejestr metadanych RLS
from app.models.commodity_code import CommodityCode  # noqa: F401 — rejestr metadanych RLS
from app.models.credit_review import CreditReview  # noqa: F401 — rejestr metadanych RLS
from app.models.customer_sop import CustomerSop  # noqa: F401 — rejestr metadanych RLS
from app.models.dangerous_good import DangerousGood  # noqa: F401 — rejestr metadanych RLS
from app.models.entity_event import EntityEvent  # noqa: F401 — rejestr metadanych RLS
from app.models.extraction_draft import ExtractionDraft  # noqa: F401 — rejestr metadanych RLS
from app.models.inbound_message import InboundMessage  # noqa: F401 — rejestr metadanych RLS
from app.models.location import (  # noqa: F401 — rejestr metadanych RLS
    Location,
    LocationZoneMember,
)
from app.models.nbp_rate import NbpRate  # noqa: F401 — rejestr metadanych RLS
from app.models.network import Network  # noqa: F401 — rejestr metadanych RLS
from app.models.network_member import NetworkMember  # noqa: F401 — rejestr metadanych RLS
from app.models.organization import Organization
from app.models.organization_setting import (  # noqa: F401 — rejestr metadanych RLS
    OrganizationSetting,
)
from app.models.party import Party  # noqa: F401 — rejestr metadanych RLS
from app.models.party_bank_account import PartyBankAccount  # noqa: F401 — rejestr metadanych RLS
from app.models.party_charge_override import (  # noqa: F401 — rejestr metadanych RLS
    PartyChargeOverride,
)
from app.models.party_contact import PartyContact  # noqa: F401 — rejestr metadanych RLS
from app.models.party_email_domain import PartyEmailDomain  # noqa: F401 — rejestr metadanych RLS
from app.models.party_role_assignment import (  # noqa: F401 — rejestr metadanych RLS
    PartyRoleAssignment,
)
from app.models.party_scorecard import PartyScorecard  # noqa: F401 — rejestr metadanych RLS
from app.models.port import Port  # noqa: F401 — rejestr metadanych RLS
from app.models.port_surcharge import PortSurcharge  # noqa: F401 — rejestr metadanych RLS
from app.models.quotation import Quotation  # noqa: F401 — rejestr metadanych RLS
from app.models.rate_line import RateLine  # noqa: F401 — rejestr metadanych RLS
from app.models.refresh_token import RefreshToken  # noqa: F401 — rejestr metadanych RLS
from app.models.table_view import TableView  # noqa: F401 — rejestr metadanych RLS
from app.models.terminal import Terminal  # noqa: F401 — rejestr metadanych RLS

_TEST_JWT_SECRET = "ci-unit-test-jwt-secret-32bytes-min"
_BACKEND_ROOT = Path(__file__).resolve().parents[1]
_test_schema_ready = False


@pytest.fixture(autouse=True)
def _jwt_secret_for_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.core.config.settings.jwt_secret", _TEST_JWT_SECRET)


ADMIN_TEST_DATABASE_URL = os.getenv(
    "ADMIN_TEST_DATABASE_URL",
    "postgresql+asyncpg://omniroute:omniroute@localhost:5432/omniroute_test",
)
TENANT_TEST_DATABASE_URL = os.getenv(
    "TENANT_TEST_DATABASE_URL",
    "postgresql+asyncpg://tenant_tester:test@localhost:5432/omniroute_test",
)


def _sync_admin_url() -> str:
    override = os.getenv("ADMIN_TEST_DATABASE_URL_SYNC")
    if override:
        return override
    return ADMIN_TEST_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)


def _ensure_roles(conn) -> None:
    conn.execute(
        text(
            """
            DO $$ BEGIN
              CREATE ROLE tenant_tester LOGIN PASSWORD 'test' NOINHERIT NOBYPASSRLS;
            EXCEPTION WHEN duplicate_object THEN NULL;
            END $$;
            """
        ),
    )
    conn.execute(
        text(
            """
            DO $$ BEGIN
              CREATE ROLE omniroute_app LOGIN PASSWORD 'omniroute'
                NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
            EXCEPTION WHEN duplicate_object THEN
              ALTER ROLE omniroute_app WITH NOSUPERUSER NOCREATEDB
                NOCREATEROLE NOINHERIT NOBYPASSRLS LOGIN;
            END $$;
            """
        ),
    )


def _grant_test_roles(conn) -> None:
    conn.execute(text("GRANT USAGE ON SCHEMA public TO tenant_tester"))
    conn.execute(text("GRANT USAGE ON SCHEMA public TO omniroute_app"))
    conn.execute(
        text(
            "GRANT SELECT, INSERT, UPDATE, DELETE "
            "ON ALL TABLES IN SCHEMA public TO tenant_tester"
        )
    )
    conn.execute(
        text(
            "GRANT SELECT, INSERT, UPDATE, DELETE "
            "ON ALL TABLES IN SCHEMA public TO omniroute_app"
        )
    )
    conn.execute(text("GRANT USAGE ON TYPE postal_range TO tenant_tester"))
    conn.execute(text("GRANT USAGE ON TYPE postal_range TO omniroute_app"))


def _upgrade_test_schema() -> None:
    ini = _BACKEND_ROOT / "alembic.ini"
    cfg = Config(str(ini))
    cfg.set_main_option("script_location", str(_BACKEND_ROOT / "alembic"))
    command.upgrade(cfg, "head")


def _ensure_test_schema() -> None:
    global _test_schema_ready
    if _test_schema_ready:
        return
    sync_url = _sync_admin_url()
    if "omniroute_test" not in sync_url:
        raise RuntimeError("Alembic testów tylko na omniroute_test, nie na żywej bazie")
    engine = create_engine(sync_url)
    with engine.begin() as conn:
        _ensure_roles(conn)
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO CURRENT_USER"))
    previous = os.environ.get("ALEMBIC_DATABASE_URL")
    os.environ["ALEMBIC_DATABASE_URL"] = sync_url
    try:
        _upgrade_test_schema()
    finally:
        if previous is None:
            os.environ.pop("ALEMBIC_DATABASE_URL", None)
        else:
            os.environ["ALEMBIC_DATABASE_URL"] = previous
    with engine.begin() as conn:
        _grant_test_roles(conn)
    engine.dispose()
    _test_schema_ready = True


def _truncate_sql(table_names: list[str]) -> str:
    quoted = ", ".join(f'"{name}"' for name in table_names)
    return f"TRUNCATE TABLE {quoted} CASCADE"


async def _truncate_public_tables(conn) -> None:
    rows = await conn.execute(
        text(
            "SELECT tablename FROM pg_tables "
            "WHERE schemaname = 'public' AND tablename <> 'alembic_version' "
            "ORDER BY tablename"
        )
    )
    tables = [row[0] for row in rows]
    if not tables:
        return
    await conn.execute(text(_truncate_sql(tables)))


@pytest_asyncio.fixture
async def engine() -> AsyncGenerator:
    _ensure_test_schema()
    admin_engine = create_async_engine(ADMIN_TEST_DATABASE_URL, pool_pre_ping=True)
    async with admin_engine.begin() as conn:
        await _truncate_public_tables(conn)
    await admin_engine.dispose()

    test_engine = create_async_engine(TENANT_TEST_DATABASE_URL, pool_pre_ping=True)
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db_session:
        yield db_session
        await db_session.rollback()


@pytest_asyncio.fixture
async def two_tenants(engine) -> dict[str, object]:
    _ = engine
    admin_engine = create_async_engine(ADMIN_TEST_DATABASE_URL, pool_pre_ping=True)
    org_a = Organization(id=uuid.uuid4(), name="Tenant A", slug=f"tenant-a-{uuid.uuid4().hex[:8]}")
    org_b = Organization(id=uuid.uuid4(), name="Tenant B", slug=f"tenant-b-{uuid.uuid4().hex[:8]}")
    user_a = AppUser(
        id=uuid.uuid4(),
        organization_id=org_a.id,
        email="a@example.com",
        display_name="User A",
    )
    user_b = AppUser(
        id=uuid.uuid4(),
        organization_id=org_b.id,
        email="b@example.com",
        display_name="User B",
    )

    session_factory = async_sessionmaker(admin_engine, expire_on_commit=False)
    async with session_factory() as db_session:
        for org in (org_a, org_b):
            await bind_tenant(db_session, org.id)
            db_session.add(org)
        await db_session.flush()

        for user in (user_a, user_b):
            await bind_tenant(db_session, user.organization_id)
            db_session.add(user)
        await db_session.commit()

    await admin_engine.dispose()

    return {
        "org_a": org_a,
        "org_b": org_b,
        "user_a": user_a,
        "user_b": user_b,
    }
