"""create quality_descent_mark catalog with RLS FORCE

Revision ID: 391_quality_descent_mark
Revises: 390_style_fidelity_mark
Create Date: 2026-09-14

AI8.2 leftover HITL powod zejscia jakosci. Nie silnik auto-zejscia. Nie L3 write.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "391_quality_descent_mark"
down_revision: str | None = "390_style_fidelity_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "quality_descent_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("descent_kind", sa.String(length=16), nullable=False),
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
            name="fk_quality_descent_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_quality_descent_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_quality_descent_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_quality_descent_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_quality_descent_mark_code",
        ),
        sa.CheckConstraint(
            "descent_kind IN ('mae', 'crps', 'brier', 'manual', 'other')",
            name="ck_quality_descent_mark_kind",
        ),
    )
    op.create_index(
        "ix_quality_descent_mark_organization_id",
        "quality_descent_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE quality_descent_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE quality_descent_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY quality_descent_mark_tenant_isolation
        ON quality_descent_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS quality_descent_mark_tenant_isolation "
        "ON quality_descent_mark",
    )
    op.drop_index(
        "ix_quality_descent_mark_organization_id",
        table_name="quality_descent_mark",
    )
    op.drop_table("quality_descent_mark")
