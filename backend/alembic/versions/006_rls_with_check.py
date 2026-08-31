"""explicit WITH CHECK on tenant isolation policies

Revision ID: 006_rls_with_check
Revises: 005_omniroute_app_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

from alembic import op

revision: str = "006_rls_with_check"
down_revision: str | None = "005_omniroute_app_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"

_POLICIES: tuple[tuple[str, str, str], ...] = (
    ("organization_tenant_isolation", "organization", f"id = {_ORG}"),
    ("app_user_tenant_isolation", "app_user", f"organization_id = {_ORG}"),
    ("table_view_tenant_isolation", "table_view", f"organization_id = {_ORG}"),
    ("extraction_draft_tenant_isolation", "extraction_draft", f"organization_id = {_ORG}"),
    ("refresh_token_tenant_isolation", "refresh_token", f"organization_id = {_ORG}"),
)


def upgrade() -> None:
    for name, table, predicate in _POLICIES:
        op.execute(
            f"ALTER POLICY {name} ON {table} USING ({predicate}) WITH CHECK ({predicate})"
        )


def downgrade() -> None:
    for name, table, predicate in _POLICIES:
        op.execute(f"ALTER POLICY {name} ON {table} USING ({predicate})")
