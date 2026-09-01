from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import delete, update
from sqlalchemy.exc import DBAPIError

from app.core.database import bind_tenant
from app.models.app_user import AppUser
from tests.patterns.tenant_isolation import (
    assert_missing_tenant_context_returns_no_rows,
    assert_tenant_cannot_read_foreign_row,
    assert_tenant_sees_only_own_rows,
)

_BASE_TENANT_POLICY_NAMES = (
    "organization_tenant_isolation",
    "app_user_tenant_isolation",
    "table_view_tenant_isolation",
    "extraction_draft_tenant_isolation",
    "refresh_token_tenant_isolation",
)
_ALL_TENANT_POLICY_NAMES = (
    *_BASE_TENANT_POLICY_NAMES,
    "charge_code_tenant_isolation",
    "rate_line_tenant_isolation",
    "charge_tenant_isolation",
    "quotation_tenant_isolation",
    "organization_setting_tenant_isolation",
    "commodity_code_tenant_isolation",
    "nbp_rate_tenant_isolation",
    "dangerous_good_tenant_isolation",
    "network_tenant_isolation",
    "party_scorecard_tenant_isolation",
    "customer_sop_tenant_isolation",
    "port_surcharge_tenant_isolation",
)


def test_conftest_tenant_policies_declare_with_check() -> None:
    source = Path("backend/tests/conftest.py").read_text(encoding="utf-8")
    for name in _ALL_TENANT_POLICY_NAMES:
        assert name in source
    assert source.count("WITH CHECK") >= 10


def test_migration_006_declares_with_check() -> None:
    source = Path("backend/alembic/versions/006_rls_with_check.py").read_text(encoding="utf-8")
    assert "WITH CHECK" in source
    for name in _BASE_TENANT_POLICY_NAMES:
        assert name in source


def test_migration_007_declares_charge_code_with_check() -> None:
    source = Path("backend/alembic/versions/007_charge_code_rls.py").read_text(encoding="utf-8")
    assert "WITH CHECK" in source
    assert "charge_code_tenant_isolation" in source
    assert "FORCE ROW LEVEL SECURITY" in source


def test_migration_008_declares_rate_line_with_check() -> None:
    source = Path("backend/alembic/versions/008_rate_line_rls.py").read_text(encoding="utf-8")
    assert "WITH CHECK" in source
    assert "rate_line_tenant_isolation" in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "rate_line_forbid_mutate" in source


def test_migration_009_declares_charge_with_check() -> None:
    source = Path("backend/alembic/versions/009_charge_rls.py").read_text(encoding="utf-8")
    assert "WITH CHECK" in source
    assert "charge_tenant_isolation" in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "charge_same_currency" in source


def test_migration_010_declares_quotation_with_check() -> None:
    source = Path("backend/alembic/versions/010_quotation_rls.py").read_text(encoding="utf-8")
    assert "WITH CHECK" in source
    assert "quotation_tenant_isolation" in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "INSERT INTO quotation" not in source
    assert "ix_rate_line_current_charge_code" in source


def test_migration_011_declares_organization_setting_with_check() -> None:
    source = Path("backend/alembic/versions/011_organization_setting_rls.py").read_text(
        encoding="utf-8",
    )
    assert "WITH CHECK" in source
    assert "organization_setting_tenant_isolation" in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "uq_organization_setting_org_key" in source


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rls_matrix_s1_select_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]
    await assert_tenant_sees_only_own_rows(session, org_a.id, {user_a.id})
    await assert_tenant_sees_only_own_rows(session, org_b.id, {user_b.id})
    await assert_tenant_cannot_read_foreign_row(session, org_a.id, user_b.id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rls_matrix_s2_insert_foreign_org_rejected(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    await bind_tenant(session, org_a.id)
    session.add(
        AppUser(
            id=uuid4(),
            organization_id=org_b.id,
            email="sneak@example.com",
            display_name="Sneak",
        )
    )
    with pytest.raises(DBAPIError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rls_matrix_s3_update_foreign_row_is_noop(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_b = two_tenants["user_b"]
    await bind_tenant(session, org_a.id)
    result = await session.execute(
        update(AppUser).where(AppUser.id == user_b.id).values(display_name="hacked")
    )
    assert result.rowcount == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rls_matrix_s4_reassign_org_rejected(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    with pytest.raises(DBAPIError):
        await session.execute(
            update(AppUser).where(AppUser.id == user_a.id).values(organization_id=org_b.id)
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rls_matrix_s5_delete_foreign_row_is_noop(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_b = two_tenants["user_b"]
    await bind_tenant(session, org_a.id)
    result = await session.execute(delete(AppUser).where(AppUser.id == user_b.id))
    assert result.rowcount == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rls_matrix_s6_missing_org_hides_rows_and_blocks_insert(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await assert_missing_tenant_context_returns_no_rows(session)
    session.add(
        AppUser(
            id=uuid4(),
            organization_id=org_a.id,
            email="no-ctx@example.com",
            display_name="No ctx",
        )
    )
    with pytest.raises(DBAPIError):
        await session.flush()
