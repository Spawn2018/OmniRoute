"""create spend_mark catalog with RLS FORCE

Revision ID: 232_spend_mark
Revises: 231_repair_playbook
Create Date: 2026-09-11

CI2 HITL rodzaj wycieku spend jako dane. Nie SQL FV vs charge. Nie marża.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "232_spend_mark"
down_revision: str | None = "231_repair_playbook"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "spend_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("leakage_kind", sa.String(length=16), nullable=False),
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
            name="fk_spend_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_spend_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_spend_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_spend_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_spend_mark_code",
        ),
        sa.CheckConstraint(
            "leakage_kind IN ('invoice', 'clause', 'other')",
            name="ck_spend_mark_leakage_kind",
        ),
    )
    op.create_index(
        "ix_spend_mark_organization_id",
        "spend_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE spend_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE spend_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY spend_mark_tenant_isolation ON spend_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS spend_mark_tenant_isolation ON spend_mark")
    op.drop_index("ix_spend_mark_organization_id", table_name="spend_mark")
    op.drop_table("spend_mark")
