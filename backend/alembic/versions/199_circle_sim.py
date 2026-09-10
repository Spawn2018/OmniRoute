"""create circle_sim catalog with RLS FORCE

Revision ID: 199_circle_sim
Revises: 198_plan_snapshot
Create Date: 2026-09-10

HITL kółko jako dane. Nie silnik ≥500k. Nie km.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "199_circle_sim"
down_revision: str | None = "198_plan_snapshot"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "circle_sim",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sim_code", sa.String(length=32), nullable=False),
        sa.Column("unload_unlocode", sa.String(length=5), nullable=False),
        sa.Column("load_unlocode", sa.String(length=5), nullable=False),
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
            name="fk_circle_sim_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_circle_sim_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "sim_code",
            name="uq_circle_sim_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_circle_sim_org_source_ref",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "unload_unlocode",
            "load_unlocode",
            name="uq_circle_sim_org_pair",
        ),
        sa.CheckConstraint(
            "sim_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_circle_sim_code",
        ),
        sa.CheckConstraint(
            "unload_unlocode <> load_unlocode",
            name="ck_circle_sim_ends_differ",
        ),
        sa.CheckConstraint(
            r"unload_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_circle_sim_unload_unlocode",
        ),
        sa.CheckConstraint(
            r"load_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_circle_sim_load_unlocode",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_circle_sim_organization_id",
        "circle_sim",
        ["organization_id"],
    )
    op.create_index(
        "ix_circle_sim_org_unload",
        "circle_sim",
        ["organization_id", "unload_unlocode"],
    )
    op.execute("ALTER TABLE circle_sim ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE circle_sim FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY circle_sim_tenant_isolation ON circle_sim
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS circle_sim_tenant_isolation ON circle_sim")
    op.drop_index("ix_circle_sim_org_unload", table_name="circle_sim")
    op.drop_index("ix_circle_sim_organization_id", table_name="circle_sim")
    op.drop_table("circle_sim")
