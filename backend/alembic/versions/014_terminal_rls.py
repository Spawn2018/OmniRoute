"""create terminal catalog and World Port Index columns on port with RLS

Revision ID: 014_terminal_rls
Revises: 013_location_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "014_terminal_rls"
down_revision: str | None = "013_location_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_HARBOR_SIZE = (
    "harbor_size IS NULL OR harbor_size IN "
    "('Very Small', 'Small', 'Medium', 'Large')"
)
_HARBOR_TYPE = (
    "harbor_type IS NULL OR harbor_type IN ("
    "'Coastal Natural', 'Coastal Breakwater', 'Coastal Tide Gate', "
    "'River Natural', 'River Basin', 'River Tide Gate', "
    "'Lake or Canal', 'Open Roadstead', 'Typhoon Harbor')"
)
_SHELTER = "shelter IS NULL OR shelter IN ('Excellent', 'Good', 'Fair', 'Poor', 'None')"


def upgrade() -> None:
    op.add_column("port", sa.Column("wpi_number", sa.Integer(), nullable=True))
    op.add_column("port", sa.Column("harbor_size", sa.String(length=16), nullable=True))
    op.add_column("port", sa.Column("harbor_type", sa.String(length=32), nullable=True))
    op.add_column("port", sa.Column("shelter", sa.String(length=16), nullable=True))
    op.add_column(
        "port",
        sa.Column("channel_depth_m", sa.Numeric(precision=6, scale=1), nullable=True),
    )
    op.add_column(
        "port",
        sa.Column("cargo_pier_depth_m", sa.Numeric(precision=6, scale=1), nullable=True),
    )
    op.add_column("port", sa.Column("wpi_source_ref", sa.String(length=256), nullable=True))
    op.create_check_constraint("ck_port_harbor_size", "port", _HARBOR_SIZE)
    op.create_check_constraint("ck_port_harbor_type", "port", _HARBOR_TYPE)
    op.create_check_constraint("ck_port_shelter", "port", _SHELTER)
    op.execute(
        "CREATE UNIQUE INDEX uq_port_org_wpi_number "
        "ON port (organization_id, wpi_number) WHERE wpi_number IS NOT NULL"
    )

    op.create_table(
        "terminal",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("port_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("isps_code", sa.String(length=32), nullable=True),
        sa.Column("operator_name", sa.String(length=256), nullable=True),
        sa.Column("lat", sa.Numeric(precision=8, scale=6), nullable=True),
        sa.Column("lng", sa.Numeric(precision=9, scale=6), nullable=True),
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
            name="fk_terminal_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "port_id"],
            ["port.organization_id", "port.id"],
            name="fk_terminal_port",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_terminal_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "port_id",
            "name",
            name="uq_terminal_org_port_name",
        ),
    )
    op.create_index("ix_terminal_organization_id", "terminal", ["organization_id"])
    op.execute(
        "CREATE UNIQUE INDEX uq_terminal_org_isps "
        "ON terminal (organization_id, isps_code) WHERE isps_code IS NOT NULL"
    )

    op.execute("ALTER TABLE terminal ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE terminal FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY terminal_tenant_isolation ON terminal
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS terminal_tenant_isolation ON terminal")
    op.execute("DROP INDEX IF EXISTS uq_terminal_org_isps")
    op.drop_index("ix_terminal_organization_id", table_name="terminal")
    op.drop_table("terminal")

    op.execute("DROP INDEX IF EXISTS uq_port_org_wpi_number")
    op.drop_constraint("ck_port_shelter", "port", type_="check")
    op.drop_constraint("ck_port_harbor_type", "port", type_="check")
    op.drop_constraint("ck_port_harbor_size", "port", type_="check")
    op.drop_column("port", "wpi_source_ref")
    op.drop_column("port", "cargo_pier_depth_m")
    op.drop_column("port", "channel_depth_m")
    op.drop_column("port", "shelter")
    op.drop_column("port", "harbor_type")
    op.drop_column("port", "harbor_size")
    op.drop_column("port", "wpi_number")
