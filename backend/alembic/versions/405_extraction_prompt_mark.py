"""create extraction_prompt_mark catalog with RLS FORCE

Revision ID: 405_extraction_prompt_mark
Revises: 404_shipper_award_mark
Create Date: 2026-09-15

AI3.1 leftover HITL prompt jako dana. Nie Instructor live. Nie wiring LLM.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "405_extraction_prompt_mark"
down_revision: str | None = "404_shipper_award_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "extraction_prompt_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("prompt_kind", sa.String(length=32), nullable=False),
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
            name="fk_extraction_prompt_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_extraction_prompt_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_extraction_prompt_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_extraction_prompt_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_extraction_prompt_mark_code",
        ),
        sa.CheckConstraint(
            "prompt_kind IN ('extract', 'system', 'other')",
            name="ck_extraction_prompt_mark_kind",
        ),
    )
    op.create_index(
        "ix_extraction_prompt_mark_organization_id",
        "extraction_prompt_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE extraction_prompt_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE extraction_prompt_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY extraction_prompt_mark_tenant_isolation ON extraction_prompt_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS extraction_prompt_mark_tenant_isolation ON extraction_prompt_mark",
    )
    op.drop_index(
        "ix_extraction_prompt_mark_organization_id",
        table_name="extraction_prompt_mark",
    )
    op.drop_table("extraction_prompt_mark")
