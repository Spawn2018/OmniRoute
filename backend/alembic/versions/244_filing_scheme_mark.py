"""create filing_scheme_mark catalog with RLS FORCE

Revision ID: 244_filing_scheme_mark
Revises: 243_bonded_mark
Create Date: 2026-09-11

G12 HITL znacznik schematu składania jako dane. Nie SENT-UE. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "244_filing_scheme_mark"
down_revision: str | None = "243_bonded_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "filing_scheme_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("scheme_kind", sa.String(length=16), nullable=False),
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
            name="fk_filing_scheme_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_filing_scheme_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_filing_scheme_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_filing_scheme_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_filing_scheme_mark_code",
        ),
        sa.CheckConstraint(
            "scheme_kind IN ('ics2', 'cbam', 'eudr', 'efti', 'other')",
            name="ck_filing_scheme_mark_scheme_kind",
        ),
    )
    op.create_index(
        "ix_filing_scheme_mark_organization_id",
        "filing_scheme_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE filing_scheme_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE filing_scheme_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY filing_scheme_mark_tenant_isolation ON filing_scheme_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS filing_scheme_mark_tenant_isolation ON filing_scheme_mark",
    )
    op.drop_index("ix_filing_scheme_mark_organization_id", table_name="filing_scheme_mark")
    op.drop_table("filing_scheme_mark")
