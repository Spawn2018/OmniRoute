"""create terminal_slot_connector catalog with RLS FORCE

Revision ID: 202_terminal_slot_connector
Revises: 201_erp_connector
Create Date: 2026-09-10

HITL capability slotu + godziny N4. Nie live T8. Nie booking.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "202_terminal_slot_connector"
down_revision: str | None = "201_erp_connector"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "terminal_slot_connector",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("connector_code", sa.String(length=32), nullable=False),
        sa.Column("terminal_code", sa.String(length=32), nullable=False),
        sa.Column("mode", sa.String(length=16), nullable=False),
        sa.Column("opens_local", sa.Time(), nullable=False),
        sa.Column("closes_local", sa.Time(), nullable=False),
        sa.Column("cutoff_local", sa.Time(), nullable=False),
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
            name="fk_terminal_slot_connector_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_terminal_slot_connector_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_terminal_slot_connector_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "terminal_code",
            name="uq_terminal_slot_connector_org_terminal",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_terminal_slot_connector_org_source_ref",
        ),
        sa.CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_terminal_slot_connector_code",
        ),
        sa.CheckConstraint(
            "terminal_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_terminal_slot_connector_terminal",
        ),
        sa.CheckConstraint(
            "mode IN ('api','email_hitl','portal_task','unsupported')",
            name="ck_terminal_slot_connector_mode",
        ),
    )
    # Lista per tenant: unique prefix albo ten indeks — nie sekwencyjne skanowanie.
    op.create_index(
        "ix_terminal_slot_connector_organization_id",
        "terminal_slot_connector",
        ["organization_id"],
    )
    op.execute("ALTER TABLE terminal_slot_connector ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE terminal_slot_connector FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY terminal_slot_connector_tenant_isolation ON terminal_slot_connector
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS terminal_slot_connector_tenant_isolation "
        "ON terminal_slot_connector"
    )
    op.drop_index(
        "ix_terminal_slot_connector_organization_id",
        table_name="terminal_slot_connector",
    )
    op.drop_table("terminal_slot_connector")
