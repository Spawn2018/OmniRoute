"""create field_confidence_mark catalog with RLS FORCE

Revision ID: 392_field_confidence_mark
Revises: 391_quality_descent_mark
Create Date: 2026-09-15

AI9.1 leftover HITL pasmo pewnosci per pole. Nie przebudowa ui-04. Nie float auto-accept.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "392_field_confidence_mark"
down_revision: str | None = "391_quality_descent_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "field_confidence_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("band_kind", sa.String(length=16), nullable=False),
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
            name="fk_field_confidence_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_field_confidence_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_field_confidence_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_field_confidence_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_field_confidence_mark_code",
        ),
        sa.CheckConstraint(
            "band_kind IN ('green', 'yellow', 'orange', 'hold', 'other')",
            name="ck_field_confidence_mark_kind",
        ),
    )
    op.create_index(
        "ix_field_confidence_mark_organization_id",
        "field_confidence_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE field_confidence_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE field_confidence_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY field_confidence_mark_tenant_isolation
        ON field_confidence_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS field_confidence_mark_tenant_isolation "
        "ON field_confidence_mark",
    )
    op.drop_index(
        "ix_field_confidence_mark_organization_id",
        table_name="field_confidence_mark",
    )
    op.drop_table("field_confidence_mark")
