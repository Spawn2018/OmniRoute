"""create charge_template catalog with RLS FORCE

Revision ID: 104_charge_template
Revises: 103_rate_card
Create Date: 2026-09-08

Szablon opłat: kolekcja kodów + daty jako dane. Nie exclusion GiST.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "104_charge_template"
down_revision: str | None = "103_rate_card"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "charge_template",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("template_code", sa.String(length=32), nullable=False),
        sa.Column("charge_code", sa.String(length=32), nullable=False),
        sa.Column("valid_from", sa.Date(), nullable=False),
        sa.Column("valid_until", sa.Date(), nullable=False),
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
            name="fk_charge_template_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "charge_code"],
            ["charge_code.organization_id", "charge_code.code"],
            name="fk_charge_template_charge_code",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_charge_template_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "template_code",
            "charge_code",
            name="uq_charge_template_org_code_member",
        ),
        sa.CheckConstraint(
            "template_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_charge_template_code_snake",
        ),
        sa.CheckConstraint(
            "charge_code ~ '^[A-Z0-9_]{2,32}$'",
            name="ck_charge_template_member_token",
        ),
        sa.CheckConstraint(
            "valid_until >= valid_from",
            name="ck_charge_template_window",
        ),
    )
    op.create_index(
        "ix_charge_template_organization_id",
        "charge_template",
        ["organization_id"],
    )
    op.create_index(
        "ix_charge_template_org_code",
        "charge_template",
        ["organization_id", "template_code"],
    )
    op.execute("ALTER TABLE charge_template ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE charge_template FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY charge_template_tenant_isolation ON charge_template
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS charge_template_tenant_isolation ON charge_template")
    op.drop_index("ix_charge_template_org_code", table_name="charge_template")
    op.drop_index("ix_charge_template_organization_id", table_name="charge_template")
    op.drop_table("charge_template")
