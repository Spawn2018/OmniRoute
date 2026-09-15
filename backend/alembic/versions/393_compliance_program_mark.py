"""create compliance_program_mark catalog with RLS FORCE

Revision ID: 393_compliance_program_mark
Revises: 392_field_confidence_mark
Create Date: 2026-09-15

AI9.2 leftover HITL stancja programu zgodnosci. Nie bajty PDF. Nie U-art50 przebudowa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "393_compliance_program_mark"
down_revision: str | None = "392_field_confidence_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "compliance_program_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("program_kind", sa.String(length=16), nullable=False),
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
            name="fk_compliance_program_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_compliance_program_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_compliance_program_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_compliance_program_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_compliance_program_mark_code",
        ),
        sa.CheckConstraint(
            "program_kind IN ('draft', 'review', 'signed', 'exempt', 'other')",
            name="ck_compliance_program_mark_kind",
        ),
    )
    op.create_index(
        "ix_compliance_program_mark_organization_id",
        "compliance_program_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE compliance_program_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE compliance_program_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY compliance_program_mark_tenant_isolation
        ON compliance_program_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS compliance_program_mark_tenant_isolation "
        "ON compliance_program_mark",
    )
    op.drop_index(
        "ix_compliance_program_mark_organization_id",
        table_name="compliance_program_mark",
    )
    op.drop_table("compliance_program_mark")
