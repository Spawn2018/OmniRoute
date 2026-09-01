import os
import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import bind_tenant
from app.models.app_user import AppUser
from app.models.base import Base
from app.models.carrier_profile import CarrierProfile  # noqa: F401 — rejestr metadanych RLS
from app.models.charge import Charge  # noqa: F401 — rejestr metadanych RLS
from app.models.charge_code import ChargeCode  # noqa: F401 — rejestr metadanych RLS
from app.models.commodity_code import CommodityCode  # noqa: F401 — rejestr metadanych RLS
from app.models.customer_sop import CustomerSop  # noqa: F401 — rejestr metadanych RLS
from app.models.dangerous_good import DangerousGood  # noqa: F401 — rejestr metadanych RLS
from app.models.extraction_draft import ExtractionDraft  # noqa: F401 — rejestr metadanych RLS
from app.models.location import (  # noqa: F401 — rejestr metadanych RLS
    Location,
    LocationZoneMember,
)
from app.models.nbp_rate import NbpRate  # noqa: F401 — rejestr metadanych RLS
from app.models.network import Network  # noqa: F401 — rejestr metadanych RLS
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
from app.models.party_scorecard import PartyScorecard  # noqa: F401 — rejestr metadanych RLS
from app.models.port import Port  # noqa: F401 — rejestr metadanych RLS
from app.models.quotation import Quotation  # noqa: F401 — rejestr metadanych RLS
from app.models.rate_line import RateLine  # noqa: F401 — rejestr metadanych RLS
from app.models.refresh_token import RefreshToken  # noqa: F401 — rejestr metadanych RLS
from app.models.table_view import TableView  # noqa: F401 — rejestr metadanych RLS
from app.models.terminal import Terminal  # noqa: F401 — rejestr metadanych RLS

_TEST_JWT_SECRET = "ci-unit-test-jwt-secret-32bytes-min"


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


async def _apply_rls_policies(conn) -> None:
    await conn.execute(text("ALTER TABLE organization ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE organization FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS organization_tenant_isolation ON organization"))
    await conn.execute(
        text(
            """
            CREATE POLICY organization_tenant_isolation ON organization
            USING (id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            """
        ),
    )
    await conn.execute(text("ALTER TABLE app_user ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE app_user FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS app_user_tenant_isolation ON app_user"))
    await conn.execute(
        text(
            """
            CREATE POLICY app_user_tenant_isolation ON app_user
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("DROP POLICY IF EXISTS app_user_login_email ON app_user"))
    await conn.execute(
        text(
            """
            CREATE POLICY app_user_login_email ON app_user
            FOR SELECT
            USING (email = NULLIF(current_setting('app.login_email', true), ''))
            """
        ),
    )
    await conn.execute(text("ALTER TABLE table_view ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE table_view FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS table_view_tenant_isolation ON table_view"))
    await conn.execute(
        text(
            """
            CREATE POLICY table_view_tenant_isolation ON table_view
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE extraction_draft ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE extraction_draft FORCE ROW LEVEL SECURITY"))
    await conn.execute(
        text("DROP POLICY IF EXISTS extraction_draft_tenant_isolation ON extraction_draft")
    )
    await conn.execute(
        text(
            """
            CREATE POLICY extraction_draft_tenant_isolation ON extraction_draft
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE refresh_token ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE refresh_token FORCE ROW LEVEL SECURITY"))
    await conn.execute(
        text("DROP POLICY IF EXISTS refresh_token_tenant_isolation ON refresh_token")
    )
    await conn.execute(
        text(
            """
            CREATE POLICY refresh_token_tenant_isolation ON refresh_token
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("DROP POLICY IF EXISTS refresh_token_by_hash ON refresh_token"))
    await conn.execute(
        text(
            """
            CREATE POLICY refresh_token_by_hash ON refresh_token
            FOR SELECT
            USING (token_hash = NULLIF(current_setting('app.refresh_hash', true), ''))
            """
        ),
    )
    await conn.execute(text("ALTER TABLE charge_code ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE charge_code FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS charge_code_tenant_isolation ON charge_code"))
    await conn.execute(
        text(
            """
            CREATE POLICY charge_code_tenant_isolation ON charge_code
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE commodity_code ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE commodity_code FORCE ROW LEVEL SECURITY"))
    await conn.execute(
        text("DROP POLICY IF EXISTS commodity_code_tenant_isolation ON commodity_code"),
    )
    await conn.execute(
        text(
            """
            CREATE POLICY commodity_code_tenant_isolation ON commodity_code
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE nbp_rate ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE nbp_rate FORCE ROW LEVEL SECURITY"))
    await conn.execute(
        text("DROP POLICY IF EXISTS nbp_rate_tenant_isolation ON nbp_rate"),
    )
    await conn.execute(
        text(
            """
            CREATE POLICY nbp_rate_tenant_isolation ON nbp_rate
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE dangerous_good ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE dangerous_good FORCE ROW LEVEL SECURITY"))
    await conn.execute(
        text("DROP POLICY IF EXISTS dangerous_good_tenant_isolation ON dangerous_good"),
    )
    await conn.execute(
        text(
            """
            CREATE POLICY dangerous_good_tenant_isolation ON dangerous_good
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE network ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE network FORCE ROW LEVEL SECURITY"))
    await conn.execute(
        text("DROP POLICY IF EXISTS network_tenant_isolation ON network"),
    )
    await conn.execute(
        text(
            """
            CREATE POLICY network_tenant_isolation ON network
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE rate_line ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE rate_line FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS rate_line_tenant_isolation ON rate_line"))
    await conn.execute(
        text(
            """
            CREATE POLICY rate_line_tenant_isolation ON rate_line
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("DROP TRIGGER IF EXISTS rate_line_forbid_mutate ON rate_line"))
    await conn.execute(text("DROP FUNCTION IF EXISTS rate_line_forbid_mutate()"))
    await conn.execute(
        text(
            """
            CREATE FUNCTION rate_line_forbid_mutate() RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
              IF TG_OP = 'DELETE' THEN
                RAISE EXCEPTION 'rate_line niemutowalny';
              END IF;
              IF NEW.organization_id IS DISTINCT FROM OLD.organization_id
                 OR NEW.charge_code IS DISTINCT FROM OLD.charge_code
                 OR NEW.amount IS DISTINCT FROM OLD.amount
                 OR NEW.currency IS DISTINCT FROM OLD.currency
                 OR NEW.source_ref IS DISTINCT FROM OLD.source_ref
                 OR NEW.created_by IS DISTINCT FROM OLD.created_by
                 OR NEW.id IS DISTINCT FROM OLD.id
              THEN
                RAISE EXCEPTION 'rate_line niemutowalny';
              END IF;
              IF OLD.superseded_by IS NOT NULL
                 AND NEW.superseded_by IS DISTINCT FROM OLD.superseded_by
              THEN
                RAISE EXCEPTION 'rate_line już zastąpiony';
              END IF;
              RETURN NEW;
            END;
            $$;
            """
        ),
    )
    await conn.execute(
        text(
            """
            CREATE TRIGGER rate_line_forbid_mutate
            BEFORE UPDATE OR DELETE ON rate_line
            FOR EACH ROW EXECUTE FUNCTION rate_line_forbid_mutate()
            """
        ),
    )
    await conn.execute(text("ALTER TABLE charge ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE charge FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS charge_tenant_isolation ON charge"))
    await conn.execute(
        text(
            """
            CREATE POLICY charge_tenant_isolation ON charge
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE quotation ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE quotation FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS quotation_tenant_isolation ON quotation"))
    await conn.execute(
        text(
            """
            CREATE POLICY quotation_tenant_isolation ON quotation
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE organization_setting ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE organization_setting FORCE ROW LEVEL SECURITY"))
    await conn.execute(
        text("DROP POLICY IF EXISTS organization_setting_tenant_isolation ON organization_setting")
    )
    await conn.execute(
        text(
            """
            CREATE POLICY organization_setting_tenant_isolation ON organization_setting
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    await conn.execute(text("ALTER TABLE port ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE port FORCE ROW LEVEL SECURITY"))
    await conn.execute(text("DROP POLICY IF EXISTS port_tenant_isolation ON port"))
    await conn.execute(
        text(
            """
            CREATE POLICY port_tenant_isolation ON port
            USING (organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid)
            WITH CHECK (
              organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
            )
            """
        ),
    )
    for table, policy in (
        ("location", "location_tenant_isolation"),
        ("location_zone_member", "location_zone_member_tenant_isolation"),
        ("terminal", "terminal_tenant_isolation"),
        ("party", "party_tenant_isolation"),
        ("party_contact", "party_contact_tenant_isolation"),
        ("party_bank_account", "party_bank_account_tenant_isolation"),
        ("party_email_domain", "party_email_domain_tenant_isolation"),
        ("party_charge_override", "party_charge_override_tenant_isolation"),
        ("carrier_profile", "carrier_profile_tenant_isolation"),
        ("party_scorecard", "party_scorecard_tenant_isolation"),
        ("customer_sop", "customer_sop_tenant_isolation"),
    ):
        await conn.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
        await conn.execute(text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"))
        await conn.execute(text(f"DROP POLICY IF EXISTS {policy} ON {table}"))
        await conn.execute(
            text(
                f"""
                CREATE POLICY {policy} ON {table}
                USING (
                  organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
                )
                WITH CHECK (
                  organization_id = NULLIF(current_setting('app.current_org', true), '')::uuid
                )
                """
            ),
        )


async def _apply_postal_zone_ddl(conn) -> None:
    """Odtwarza to, czego metadane ORM nie niosą: własny typ range i wykluczanie nakładek.

    Lustro migracji `013_location_rls` — typ `postal_range` z kolacją "C" oraz
    kolumna generowana `postal_span` żyją wyłącznie w bazie.
    """
    await conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist"))
    await conn.execute(
        text(
            """
            DO $$ BEGIN
              CREATE TYPE postal_range AS RANGE (subtype = text, collation = "C");
            EXCEPTION WHEN duplicate_object THEN NULL;
            END $$;
            """
        ),
    )
    await conn.execute(
        text(
            "CREATE UNIQUE INDEX uq_location_org_code ON location (organization_id, code) "
            "WHERE code IS NOT NULL"
        ),
    )
    await conn.execute(
        text(
            "ALTER TABLE location_zone_member ADD COLUMN postal_span postal_range "
            "GENERATED ALWAYS AS (postal_range(postal_from, postal_to, '[]')) STORED"
        ),
    )
    await conn.execute(
        text(
            """
            ALTER TABLE location_zone_member ADD CONSTRAINT ex_zone_member_no_overlap
            EXCLUDE USING gist (
              organization_id WITH =, country_code WITH =, postal_span WITH &&
            )
            """
        ),
    )


@pytest_asyncio.fixture
async def engine() -> AsyncGenerator:
    admin_engine = create_async_engine(ADMIN_TEST_DATABASE_URL, pool_pre_ping=True)

    async with admin_engine.begin() as conn:
        await conn.execute(
            text(
                """
                DO $$ BEGIN
                  CREATE ROLE tenant_tester LOGIN PASSWORD 'test' NOINHERIT NOBYPASSRLS;
                EXCEPTION WHEN duplicate_object THEN NULL;
                END $$;
                """
            ),
        )
        await conn.execute(
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
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await _apply_postal_zone_ddl(conn)
        await _apply_rls_policies(conn)
        await conn.execute(text("GRANT USAGE ON SCHEMA public TO tenant_tester"))
        await conn.execute(text("GRANT USAGE ON SCHEMA public TO omniroute_app"))
        await conn.execute(
            text(
                "GRANT SELECT, INSERT, UPDATE, DELETE "
                "ON ALL TABLES IN SCHEMA public TO tenant_tester"
            )
        )
        await conn.execute(
            text(
                "GRANT SELECT, INSERT, UPDATE, DELETE "
                "ON ALL TABLES IN SCHEMA public TO omniroute_app"
            )
        )

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
async def two_tenants() -> dict[str, object]:
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
