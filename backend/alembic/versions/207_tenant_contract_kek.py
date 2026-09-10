"""create tenant_contract_kek catalog with RLS FORCE

Revision ID: 207_tenant_contract_kek
Revises: 206_customer_contract_blob
Create Date: 2026-09-10

HITL znacznik owijki (password|kms) jako dane. Nie klucz. Nie bajty. Nie KMS.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "207_tenant_contract_kek"
down_revision: str | None = "206_customer_contract_blob"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tenant_contract_kek",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kek_code", sa.String(length=32), nullable=False),
        sa.Column("wrap_kind", sa.String(length=16), nullable=False),
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
            name="fk_tenant_contract_kek_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tenant_contract_kek_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "kek_code",
            name="uq_tenant_contract_kek_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tenant_contract_kek_org_source_ref",
        ),
        sa.CheckConstraint(
            "kek_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tenant_contract_kek_code",
        ),
        sa.CheckConstraint(
            "wrap_kind IN ('password', 'kms')",
            name="ck_tenant_contract_kek_wrap",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_tenant_contract_kek_organization_id",
        "tenant_contract_kek",
        ["organization_id"],
    )
    op.execute("ALTER TABLE tenant_contract_kek ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tenant_contract_kek FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tenant_contract_kek_tenant_isolation ON tenant_contract_kek
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS tenant_contract_kek_tenant_isolation ON tenant_contract_kek")
    op.drop_index("ix_tenant_contract_kek_organization_id", table_name="tenant_contract_kek")
    op.drop_table("tenant_contract_kek")
