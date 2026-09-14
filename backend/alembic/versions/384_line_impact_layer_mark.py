"""create line_impact_layer_mark catalog with RLS FORCE

Revision ID: 384_line_impact_layer_mark
Revises: 383_ops_room_mark
Create Date: 2026-09-14

BR7.1 HITL katalog warstwy liczonej wpływu na linię. Nie SQL. Nie EBITDA.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "384_line_impact_layer_mark"
down_revision: str | None = "383_ops_room_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "line_impact_layer_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("layer_kind", sa.String(length=16), nullable=False),
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
            name="fk_line_impact_layer_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_line_impact_layer_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_line_impact_layer_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_line_impact_layer_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_line_impact_layer_mark_code",
        ),
        sa.CheckConstraint(
            "layer_kind IN ('scored', 'forecast', 'actual', 'other')",
            name="ck_line_impact_layer_mark_kind",
        ),
    )
    op.create_index(
        "ix_line_impact_layer_mark_organization_id",
        "line_impact_layer_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE line_impact_layer_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE line_impact_layer_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY line_impact_layer_mark_tenant_isolation
        ON line_impact_layer_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS line_impact_layer_mark_tenant_isolation ON line_impact_layer_mark",
    )
    op.drop_index(
        "ix_line_impact_layer_mark_organization_id",
        table_name="line_impact_layer_mark",
    )
    op.drop_table("line_impact_layer_mark")
