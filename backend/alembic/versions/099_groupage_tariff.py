"""create groupage_tariff on postal zone with RLS FORCE

Revision ID: 099_groupage_tariff
Revises: 098_cod_instruction
Create Date: 2026-09-08

Cennik drobnicy: próg wagi na strefie. Decimal. Nie silnik P1.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "099_groupage_tariff"
down_revision: str | None = "098_cod_instruction"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "groupage_tariff",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("location_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tariff_code", sa.String(length=32), nullable=False),
        sa.Column("chargeable_weight", sa.Numeric(14, 4), nullable=False),
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
            name="fk_groupage_tariff_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "location_id"],
            ["location.organization_id", "location.id"],
            name="fk_groupage_tariff_location",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_groupage_tariff_org_id"),
        sa.CheckConstraint("amount > 0", name="ck_groupage_tariff_amount_positive"),
        sa.CheckConstraint(
            "chargeable_weight > 0",
            name="ck_groupage_tariff_weight_positive",
        ),
        sa.CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_groupage_tariff_currency_iso"),
    )
    op.create_index(
        "ix_groupage_tariff_organization_id",
        "groupage_tariff",
        ["organization_id"],
    )
    op.create_index(
        "ix_groupage_tariff_org_location",
        "groupage_tariff",
        ["organization_id", "location_id"],
    )
    op.execute("ALTER TABLE groupage_tariff ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE groupage_tariff FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY groupage_tariff_tenant_isolation ON groupage_tariff
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS groupage_tariff_tenant_isolation ON groupage_tariff")
    op.drop_index("ix_groupage_tariff_org_location", table_name="groupage_tariff")
    op.drop_index("ix_groupage_tariff_organization_id", table_name="groupage_tariff")
    op.drop_table("groupage_tariff")
