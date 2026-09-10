"""create customer_contract header catalog with RLS FORCE

Revision ID: 205_customer_contract
Revises: 204_exchange_connector
Create Date: 2026-09-10

HITL nagłówek umowy klienta jako dane. Nie treść. Nie ciphertext. Nie KEK.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "205_customer_contract"
down_revision: str | None = "204_exchange_connector"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "customer_contract",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("contract_code", sa.String(length=32), nullable=False),
        sa.Column("shipper_label", sa.String(length=128), nullable=False),
        sa.Column("their_customer_label", sa.String(length=128), nullable=False),
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
            name="fk_customer_contract_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_customer_contract_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "contract_code",
            name="uq_customer_contract_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_customer_contract_org_source_ref",
        ),
        sa.CheckConstraint(
            "contract_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_customer_contract_code",
        ),
        sa.CheckConstraint(
            "char_length(shipper_label) BETWEEN 1 AND 128",
            name="ck_customer_contract_shipper",
        ),
        sa.CheckConstraint(
            "char_length(their_customer_label) BETWEEN 1 AND 128",
            name="ck_customer_contract_customer",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_customer_contract_organization_id",
        "customer_contract",
        ["organization_id"],
    )
    op.execute("ALTER TABLE customer_contract ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE customer_contract FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY customer_contract_tenant_isolation ON customer_contract
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS customer_contract_tenant_isolation ON customer_contract")
    op.drop_index("ix_customer_contract_organization_id", table_name="customer_contract")
    op.drop_table("customer_contract")
