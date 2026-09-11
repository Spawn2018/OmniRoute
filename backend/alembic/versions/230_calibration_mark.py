"""create calibration_mark catalog with RLS FORCE

Revision ID: 230_calibration_mark
Revises: 229_clause_notice
Create Date: 2026-09-11

CI7 HITL znacznik gotowości próbki jako dane. Nie MAE SQL. Nie float.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "230_calibration_mark"
down_revision: str | None = "229_clause_notice"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "calibration_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("sample_ready", sa.String(length=16), nullable=False),
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
            name="fk_calibration_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_calibration_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_calibration_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_calibration_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_calibration_mark_code",
        ),
        sa.CheckConstraint(
            "sample_ready IN ('ready', 'pending')",
            name="ck_calibration_mark_sample_ready",
        ),
    )
    op.create_index(
        "ix_calibration_mark_organization_id",
        "calibration_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE calibration_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE calibration_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY calibration_mark_tenant_isolation ON calibration_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS calibration_mark_tenant_isolation ON calibration_mark"
    )
    op.drop_index(
        "ix_calibration_mark_organization_id",
        table_name="calibration_mark",
    )
    op.drop_table("calibration_mark")
