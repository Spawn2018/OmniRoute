"""create container catalog with RLS FORCE

Revision ID: 093_container
Revises: 092_trip
Create Date: 2026-09-08

Kontener ISO 6346 per tenant. Nie booking armatorski.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "093_container"
down_revision: str | None = "092_trip"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "container",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("container_no", sa.String(length=11), nullable=False),
        sa.Column("iso_size_type", sa.String(length=4), nullable=False),
        sa.Column("shipment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_ref", sa.Text(), nullable=False),
        sa.Column("superseded_by", postgresql.UUID(as_uuid=True), nullable=True),
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
            name="fk_container_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_container_shipment",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by"],
            ["container.id"],
            name="fk_container_superseded_by",
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_container_organization_id", "container", ["organization_id"])
    op.create_index("ix_container_org_type", "container", ["organization_id", "iso_size_type"])
    op.execute("ALTER TABLE container ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE container FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY container_tenant_isolation
        ON container
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS container_tenant_isolation ON container")
    op.drop_index("ix_container_org_type", table_name="container")
    op.drop_index("ix_container_organization_id", table_name="container")
    op.drop_table("container")
