"""create executive_mark catalog with RLS FORCE

Revision ID: 142_executive_mark
Revises: 141_memory_edge
Create Date: 2026-09-09

HITL rodzaj pytania zarządu. Nie suma. Nie zdania z agregatów.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "142_executive_mark"
down_revision: str | None = "141_memory_edge"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "executive_mark",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_kind", sa.String(length=16), nullable=False),
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
            name="fk_executive_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_executive_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_executive_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "question_kind IN ("
            "'loss','lane','risk','cash','other'"
            ")",
            name="ck_executive_mark_kind",
        ),
    )
    # Lista per tenant — RLS filtruje organization_id; unique source_ref nie zastępuje tego skanu.
    op.create_index("ix_executive_mark_organization_id", "executive_mark", ["organization_id"])
    op.execute("ALTER TABLE executive_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE executive_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY executive_mark_tenant_isolation ON executive_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS executive_mark_tenant_isolation ON executive_mark")
    op.drop_index("ix_executive_mark_organization_id", table_name="executive_mark")
    op.drop_table("executive_mark")
