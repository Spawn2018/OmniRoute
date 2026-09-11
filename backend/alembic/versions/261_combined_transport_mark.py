"""create combined_transport_mark catalog with RLS FORCE

Revision ID: 261_combined_transport_mark
Revises: 260_cabotage_mark
Create Date: 2026-09-12

EXP2.12 HITL reżim combined transport jako dane. Nie silnik. Nie Mobility Package.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "261_combined_transport_mark"
down_revision: str | None = "260_cabotage_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "combined_transport_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("regime_kind", sa.String(length=16), nullable=False),
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
        sa.Column("created_by", PGUUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_combined_transport_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_combined_transport_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_combined_transport_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_combined_transport_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_combined_transport_mark_code",
        ),
        sa.CheckConstraint(
            "regime_kind IN ('combined', 'mobility', 'piggyback', 'other')",
            name="ck_combined_transport_mark_regime_kind",
        ),
    )
    op.create_index(
        "ix_combined_transport_mark_organization_id",
        "combined_transport_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE combined_transport_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE combined_transport_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY combined_transport_mark_tenant_isolation ON combined_transport_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS combined_transport_mark_tenant_isolation ON combined_transport_mark",
    )
    op.drop_index(
        "ix_combined_transport_mark_organization_id",
        table_name="combined_transport_mark",
    )
    op.drop_table("combined_transport_mark")
