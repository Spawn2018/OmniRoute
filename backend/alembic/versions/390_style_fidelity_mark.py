"""create style_fidelity_mark catalog with RLS FORCE

Revision ID: 390_style_fidelity_mark
Revises: 389_style_cascade_mark
Create Date: 2026-09-14

AI8.1 HITL katalog stancji bramki fidelity. Nie wyliczanie progu. Nie ocena osoby.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "390_style_fidelity_mark"
down_revision: str | None = "389_style_cascade_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "style_fidelity_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("fidelity_kind", sa.String(length=16), nullable=False),
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
            name="fk_style_fidelity_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_style_fidelity_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_style_fidelity_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_style_fidelity_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_style_fidelity_mark_code",
        ),
        sa.CheckConstraint(
            "fidelity_kind IN ('pass', 'hold', 'reject', 'exempt', 'other')",
            name="ck_style_fidelity_mark_kind",
        ),
    )
    op.create_index(
        "ix_style_fidelity_mark_organization_id",
        "style_fidelity_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE style_fidelity_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE style_fidelity_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY style_fidelity_mark_tenant_isolation
        ON style_fidelity_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS style_fidelity_mark_tenant_isolation "
        "ON style_fidelity_mark",
    )
    op.drop_index(
        "ix_style_fidelity_mark_organization_id",
        table_name="style_fidelity_mark",
    )
    op.drop_table("style_fidelity_mark")
