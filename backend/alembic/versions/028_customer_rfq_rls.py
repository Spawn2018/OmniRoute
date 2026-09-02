"""create customer_rfq with same-tenant inbound_message FK

Revision ID: 028_customer_rfq_rls
Revises: 027_inbound_message_party
Create Date: 2026-09-03
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "028_customer_rfq_rls"
down_revision: str | None = "027_inbound_message_party"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_inbound_message_org_id",
        "inbound_message",
        ["organization_id", "id"],
    )
    op.create_table(
        "customer_rfq",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("inbound_message_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_ref", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=8), nullable=False),
        sa.Column("party_id", postgresql.UUID(as_uuid=True), nullable=True),
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
            name="fk_customer_rfq_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "inbound_message_id"],
            ["inbound_message.organization_id", "inbound_message.id"],
            name="fk_customer_rfq_inbound_message",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_customer_rfq_party",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "inbound_message_id",
            name="uq_customer_rfq_org_message",
        ),
        sa.CheckConstraint("status = 'draft'", name="ck_customer_rfq_status_draft"),
        sa.CheckConstraint(
            "source_ref ~ '^(fixture|synth)://'",
            name="ck_customer_rfq_source_fixture",
        ),
    )
    op.create_index("ix_customer_rfq_organization_id", "customer_rfq", ["organization_id"])
    op.create_index(
        "ix_customer_rfq_org_created",
        "customer_rfq",
        ["organization_id", "created_at"],
    )
    op.execute("ALTER TABLE customer_rfq ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE customer_rfq FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY customer_rfq_tenant_isolation ON customer_rfq
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS customer_rfq_tenant_isolation ON customer_rfq")
    op.drop_index("ix_customer_rfq_org_created", table_name="customer_rfq")
    op.drop_index("ix_customer_rfq_organization_id", table_name="customer_rfq")
    op.drop_table("customer_rfq")
    op.drop_constraint("uq_inbound_message_org_id", "inbound_message", type_="unique")
