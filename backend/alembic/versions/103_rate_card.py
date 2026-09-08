"""create rate_card catalog with RLS FORCE

Revision ID: 103_rate_card
Revises: 102_document_template
Create Date: 2026-09-08

Karta stawek: applies_when jako dane + Decimal. Nie silnik WHEN/IF.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "103_rate_card"
down_revision: str | None = "102_document_template"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "rate_card",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("card_code", sa.String(length=32), nullable=False),
        sa.Column("applies_when", sa.String(length=512), nullable=False),
        sa.Column("amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), nullable=False),
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
            name="fk_rate_card_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_rate_card_org_id"),
        sa.CheckConstraint("amount > 0", name="ck_rate_card_amount_positive"),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_rate_card_currency_iso"),
        sa.CheckConstraint("char_length(applies_when) >= 1", name="ck_rate_card_when_len"),
        sa.CheckConstraint(
            "card_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_rate_card_code_snake",
        ),
    )
    op.create_index(
        "ix_rate_card_organization_id",
        "rate_card",
        ["organization_id"],
    )
    op.create_index(
        "ix_rate_card_org_code",
        "rate_card",
        ["organization_id", "card_code"],
    )
    op.execute("ALTER TABLE rate_card ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE rate_card FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY rate_card_tenant_isolation ON rate_card
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS rate_card_tenant_isolation ON rate_card")
    op.drop_index("ix_rate_card_org_code", table_name="rate_card")
    op.drop_index("ix_rate_card_organization_id", table_name="rate_card")
    op.drop_table("rate_card")
