"""create impact_edge_mark catalog with RLS FORCE

Revision ID: 410_impact_edge_mark
Revises: 409_impact_node_mark
Create Date: 2026-09-15

AI6.0 HITL krawedz kaskady Business Impact Graph. Nie SQL grafu. Nie EBITDA.
Nie FK do impact_node_mark.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "410_impact_edge_mark"
down_revision: str | None = "409_impact_node_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_KIND = (
    "'shipment', 'inventory', 'sku', 'line', 'order', 'revenue', 'margin', 'cash', 'other'"
)


def upgrade() -> None:
    op.create_table(
        "impact_edge_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("from_kind", sa.String(length=16), nullable=False),
        sa.Column("to_kind", sa.String(length=16), nullable=False),
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
            name="fk_impact_edge_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_impact_edge_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_impact_edge_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_impact_edge_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_impact_edge_mark_code",
        ),
        sa.CheckConstraint(
            f"from_kind IN ({_KIND})",
            name="ck_impact_edge_mark_from_kind",
        ),
        sa.CheckConstraint(
            f"to_kind IN ({_KIND})",
            name="ck_impact_edge_mark_to_kind",
        ),
    )
    op.create_index(
        "ix_impact_edge_mark_organization_id",
        "impact_edge_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE impact_edge_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE impact_edge_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY impact_edge_mark_tenant_isolation ON impact_edge_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS impact_edge_mark_tenant_isolation ON impact_edge_mark",
    )
    op.drop_index("ix_impact_edge_mark_organization_id", table_name="impact_edge_mark")
    op.drop_table("impact_edge_mark")
