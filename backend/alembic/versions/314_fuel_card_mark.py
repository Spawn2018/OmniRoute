"""create fuel_card_mark catalog with RLS FORCE

Revision ID: 314_fuel_card_mark
Revises: 313_impersonate_guard_mark
Create Date: 2026-09-12

EXP2.14 HITL znacznik karty paliwowej / anomalia. Nie live fuel. Nie litry.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "314_fuel_card_mark"
down_revision: str | None = "313_impersonate_guard_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "fuel_card_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("card_kind", sa.String(length=16), nullable=False),
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
            name="fk_fuel_card_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_fuel_card_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_fuel_card_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_fuel_card_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_fuel_card_mark_code",
        ),
        sa.CheckConstraint(
            "card_kind IN ('fuel', 'anomaly', 'other')",
            name="ck_fuel_card_mark_card_kind",
        ),
    )
    op.create_index(
        "ix_fuel_card_mark_organization_id",
        "fuel_card_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE fuel_card_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE fuel_card_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY fuel_card_mark_tenant_isolation ON fuel_card_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS fuel_card_mark_tenant_isolation ON fuel_card_mark",
    )
    op.drop_index(
        "ix_fuel_card_mark_organization_id",
        table_name="fuel_card_mark",
    )
    op.drop_table("fuel_card_mark")
