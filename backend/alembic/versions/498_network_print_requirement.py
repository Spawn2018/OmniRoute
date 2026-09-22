"""create network_print_requirement catalog with RLS FORCE

Revision ID: 498_network_print_requirement
Revises: 497_groupage_tariff_volume
Create Date: 2026-09-22

D9c HITL wymóg wydruku sieci. Nie 409. Nie PDF. Nie QR.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "498_network_print_requirement"
down_revision: str | None = "497_groupage_tariff_volume"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "network_print_requirement",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("requirement_code", sa.String(length=32), nullable=False),
        sa.Column("network_label", sa.String(length=64), nullable=False),
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
            name="fk_network_print_requirement_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_network_print_requirement_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "requirement_code",
            name="uq_network_print_requirement_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_network_print_requirement_org_source_ref",
        ),
        sa.CheckConstraint(
            "requirement_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_network_print_requirement_code",
        ),
        sa.CheckConstraint(
            "char_length(btrim(network_label)) BETWEEN 1 AND 64",
            name="ck_network_print_requirement_label",
        ),
    )
    op.create_index(
        "ix_network_print_requirement_organization_id",
        "network_print_requirement",
        ["organization_id"],
    )
    op.execute("ALTER TABLE network_print_requirement ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE network_print_requirement FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY network_print_requirement_tenant_isolation
        ON network_print_requirement
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS network_print_requirement_tenant_isolation "
        "ON network_print_requirement",
    )
    op.drop_index(
        "ix_network_print_requirement_organization_id",
        table_name="network_print_requirement",
    )
    op.drop_table("network_print_requirement")
