"""create margin_floor catalog with RLS FORCE

Revision ID: 417_margin_floor
Revises: 416_kpi_definition_mark
Create Date: 2026-09-16

N6 HITL podłoga marży Decimal + para UN/LOCODE. Bez egzekucji na charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "417_margin_floor"
down_revision: str | None = "416_kpi_definition_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"
_CCY = r"^[A-Z]{3}$"
_UNLO = r"^[A-Z]{2}[A-Z0-9]{3}$"


def upgrade() -> None:
    op.create_table(
        "margin_floor",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("floor_code", sa.String(length=32), nullable=False),
        sa.Column("origin_unlocode", sa.String(length=5), nullable=False),
        sa.Column("destination_unlocode", sa.String(length=5), nullable=False),
        sa.Column("floor_amount", sa.Numeric(14, 4), nullable=False),
        sa.Column("floor_currency", sa.CHAR(length=3), nullable=False),
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
            name="fk_margin_floor_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_margin_floor_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "floor_code",
            name="uq_margin_floor_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_margin_floor_org_source_ref",
        ),
        sa.CheckConstraint(
            f"floor_code ~ '{_SNAKE}'",
            name="ck_margin_floor_code",
        ),
        sa.CheckConstraint(
            f"floor_currency ~ '{_CCY}'",
            name="ck_margin_floor_currency",
        ),
        sa.CheckConstraint(
            f"origin_unlocode ~ '{_UNLO}'",
            name="ck_margin_floor_origin_unlocode",
        ),
        sa.CheckConstraint(
            f"destination_unlocode ~ '{_UNLO}'",
            name="ck_margin_floor_destination_unlocode",
        ),
        sa.CheckConstraint(
            "origin_unlocode <> destination_unlocode",
            name="ck_margin_floor_unlocode_pair",
        ),
    )
    op.create_index(
        "ix_margin_floor_organization_id",
        "margin_floor",
        ["organization_id"],
    )
    op.execute("ALTER TABLE margin_floor ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE margin_floor FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY margin_floor_tenant_isolation ON margin_floor
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS margin_floor_tenant_isolation ON margin_floor",
    )
    op.drop_index(
        "ix_margin_floor_organization_id",
        table_name="margin_floor",
    )
    op.drop_table("margin_floor")
