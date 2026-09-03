"""create fraud_flag on party with RLS FORCE

Revision ID: 070_fraud_flag_rls
Revises: 069_cargo_claim_rls
Create Date: 2026-09-04

Flaga oszustwa na kontrahencie. Nie kwota. Nie scoring osoby.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "070_fraud_flag_rls"
down_revision: str | None = "069_cargo_claim_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "fraud_flag",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("flag_kind", sa.String(length=16), nullable=False),
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
            name="fk_fraud_flag_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_fraud_flag_party",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "flag_kind IN ('billing', 'document', 'other')",
            name="ck_fraud_flag_kind",
        ),
    )
    op.create_index(
        "ix_fraud_flag_organization_id",
        "fraud_flag",
        ["organization_id"],
    )
    op.create_index(
        "ix_fraud_flag_org_party",
        "fraud_flag",
        ["organization_id", "party_id"],
    )
    op.execute("ALTER TABLE fraud_flag ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE fraud_flag FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY fraud_flag_tenant_isolation ON fraud_flag
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS fraud_flag_tenant_isolation ON fraud_flag")
    op.drop_index("ix_fraud_flag_org_party", table_name="fraud_flag")
    op.drop_index("ix_fraud_flag_organization_id", table_name="fraud_flag")
    op.drop_table("fraud_flag")
