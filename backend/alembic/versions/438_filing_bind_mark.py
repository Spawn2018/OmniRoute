"""create filing_bind_mark catalog with RLS FORCE

Revision ID: 438_filing_bind_mark
Revises: 437_doc_kind_match_mark
Create Date: 2026-09-18

C1 HITL filing_bind_mark. Nie FK shipment. Nie PUESC.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "438_filing_bind_mark"
down_revision: str | None = "437_doc_kind_match_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "filing_bind_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("bind_kind", sa.String(length=16), nullable=False),
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
            name="fk_filing_bind_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_filing_bind_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id", "mark_code", name="uq_filing_bind_mark_org_code"
        ),
        sa.UniqueConstraint(
            "organization_id", "source_ref", name="uq_filing_bind_mark_org_source_ref"
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_filing_bind_mark_code",
        ),
        sa.CheckConstraint(
            "bind_kind IN ('shipment', 'scheme', 'both', 'other')",
            name="ck_filing_bind_mark_bind_kind",
        ),
    )
    op.create_index(
        "ix_filing_bind_mark_organization_id",
        "filing_bind_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE filing_bind_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE filing_bind_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY filing_bind_mark_tenant_isolation
        ON filing_bind_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS filing_bind_mark_tenant_isolation ON filing_bind_mark"
    )
    op.drop_index(
        "ix_filing_bind_mark_organization_id", table_name="filing_bind_mark"
    )
    op.drop_table("filing_bind_mark")
