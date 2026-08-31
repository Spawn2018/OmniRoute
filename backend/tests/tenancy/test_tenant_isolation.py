import pytest

from tests.patterns.tenant_isolation import (
    assert_missing_tenant_context_returns_no_rows,
    assert_tenant_cannot_read_foreign_row,
    assert_tenant_sees_only_own_rows,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_app_user_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await assert_tenant_sees_only_own_rows(session, org_a.id, {user_a.id})
    await assert_tenant_sees_only_own_rows(session, org_b.id, {user_b.id})
    await assert_tenant_cannot_read_foreign_row(session, org_a.id, user_b.id)
    await assert_tenant_cannot_read_foreign_row(session, org_b.id, user_a.id)
    await assert_missing_tenant_context_returns_no_rows(session)
