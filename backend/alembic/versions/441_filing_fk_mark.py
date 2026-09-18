"""create filing_fk_mark catalog with RLS FORCE

Revision ID: 441_filing_fk_mark
Revises: 440_blocks_create_enf_mark
Create Date: 2026-09-18

C1 HITL filing_fk_mark. Nie live FK. Nie PUESC.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "441_filing_fk_mark"
down_revision: str | None = "440_blocks_create_enf_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "filing_fk_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("fk_kind", sa.String(length=16), nullable=False),
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
            name="fk_filing_fk_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_filing_fk_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_filing_fk_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_filing_fk_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_filing_fk_mark_code",
        ),
        sa.CheckConstraint(
            "fk_kind IN ('shipment', 'scheme', 'other')",
            name="ck_filing_fk_mark_fk_kind",
        ),
    )
    op.create_index(
        "ix_filing_fk_mark_organization_id",
        "filing_fk_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE filing_fk_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE filing_fk_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY filing_fk_mark_tenant_isolation
        ON filing_fk_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS filing_fk_mark_tenant_isolation ON filing_fk_mark"
    )
    op.drop_index(
        "ix_filing_fk_mark_organization_id",
        table_name="filing_fk_mark",
    )
    op.drop_table("filing_fk_mark")
