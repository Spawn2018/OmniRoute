"""create gdpr_request with RLS FORCE

Revision ID: 064_gdpr_request_rls
Revises: 063_collective_invoice_rls
Create Date: 2026-09-03

Wniosek RODO na koncie tenanta. Nie DPIA. Nie kasowanie wiersza app_user.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "064_gdpr_request_rls"
down_revision: str | None = "063_collective_invoice_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_app_user_org_id",
        "app_user",
        ["organization_id", "id"],
    )
    op.create_table(
        "gdpr_request",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("app_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_kind", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("source_ref", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_gdpr_request_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "app_user_id"],
            ["app_user.organization_id", "app_user.id"],
            name="fk_gdpr_request_app_user",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "request_kind IN ('access', 'erasure')",
            name="ck_gdpr_request_kind",
        ),
        sa.CheckConstraint(
            "status IN ('open', 'fulfilled')",
            name="ck_gdpr_request_status",
        ),
    )
    op.create_index(
        "ix_gdpr_request_organization_id",
        "gdpr_request",
        ["organization_id"],
    )
    op.create_index(
        "ix_gdpr_request_org_user",
        "gdpr_request",
        ["organization_id", "app_user_id"],
    )
    op.create_index(
        "uq_gdpr_request_open",
        "gdpr_request",
        ["organization_id", "app_user_id", "request_kind"],
        unique=True,
        postgresql_where=sa.text("status = 'open'"),
    )
    op.execute("ALTER TABLE gdpr_request ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE gdpr_request FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY gdpr_request_tenant_isolation
        ON gdpr_request
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS gdpr_request_tenant_isolation ON gdpr_request")
    op.drop_index("uq_gdpr_request_open", table_name="gdpr_request")
    op.drop_index("ix_gdpr_request_org_user", table_name="gdpr_request")
    op.drop_index("ix_gdpr_request_organization_id", table_name="gdpr_request")
    op.drop_table("gdpr_request")
    op.drop_constraint("uq_app_user_org_id", "app_user", type_="unique")
