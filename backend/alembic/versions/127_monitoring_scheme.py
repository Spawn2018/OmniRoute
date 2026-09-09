"""create monitoring_scheme catalog with RLS FORCE

Revision ID: 127_monitoring_scheme
Revises: 126_kreptd_licence
Create Date: 2026-09-09

HITL monitoring scheme catalog: scheme_code + source_ref. Nie SENT XML. Nie PUESC.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "127_monitoring_scheme"
down_revision: str | None = "126_kreptd_licence"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "monitoring_scheme",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scheme_code", sa.String(length=32), nullable=False),
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
            name="fk_monitoring_scheme_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_monitoring_scheme_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "scheme_code",
            name="uq_monitoring_scheme_org_code",
        ),
        sa.CheckConstraint(
            "scheme_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_monitoring_scheme_code",
        ),
    )
    op.create_index(
        "ix_monitoring_scheme_organization_id",
        "monitoring_scheme",
        ["organization_id"],
    )
    op.execute("ALTER TABLE monitoring_scheme ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE monitoring_scheme FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY monitoring_scheme_tenant_isolation ON monitoring_scheme
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS monitoring_scheme_tenant_isolation ON monitoring_scheme")
    op.drop_index("ix_monitoring_scheme_organization_id", table_name="monitoring_scheme")
    op.drop_table("monitoring_scheme")
