"""create spot_contract_mark catalog with RLS FORCE

Revision ID: 338_spot_contract_mark
Revises: 337_diversion_mark
Create Date: 2026-09-13

EXP1 HITL spot_contract_mark. Nie FK quotation. Nie cargo_value.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "338_spot_contract_mark"
down_revision: str | None = "337_diversion_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "spot_contract_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("deal_kind", sa.String(length=16), nullable=False),
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
            name="fk_spot_contract_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_spot_contract_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_spot_contract_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_spot_contract_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_spot_contract_mark_code",
        ),
        sa.CheckConstraint(
            "deal_kind IN ('spot', 'contract', 'other')",
            name="ck_spot_contract_mark_deal_kind",
        ),
    )
    op.create_index(
        "ix_spot_contract_mark_organization_id",
        "spot_contract_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE spot_contract_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE spot_contract_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY spot_contract_mark_tenant_isolation ON spot_contract_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS spot_contract_mark_tenant_isolation ON spot_contract_mark",
    )
    op.drop_index(
        "ix_spot_contract_mark_organization_id",
        table_name="spot_contract_mark",
    )
    op.drop_table("spot_contract_mark")
