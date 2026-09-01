"""create location catalog and tariff zones with RLS

Revision ID: 013_location_rls
Revises: 012_port_rls
Create Date: 2026-09-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "013_location_rls"
down_revision: str | None = "012_port_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    # Kolacja "C" jest warunkiem poprawności, nie stylem: domyślna kolacja PL/DE
    # sortuje inaczej niż bajtowo i zakresy pocztowe przestałyby się domykać.
    op.execute('CREATE TYPE postal_range AS RANGE (subtype = text, collation = "C")')

    # 012 dał tylko unikat po unlocode; FK tenant-safe potrzebuje nośnika na (organization_id, id).
    op.create_unique_constraint("uq_port_org_id", "port", ["organization_id", "id"])

    op.create_table(
        "location",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=True),
        sa.Column("port_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("country_code", sa.String(length=2), nullable=True),
        sa.Column("city", sa.String(length=128), nullable=True),
        sa.Column("address_line", sa.String(length=256), nullable=True),
        sa.Column("postal_code", sa.String(length=16), nullable=True),
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
            name="fk_location_organization_id",
            ondelete="RESTRICT",
        ),
        # Kolumna złożona, żeby baza odrzuciła wskazanie portu innego tenanta.
        sa.ForeignKeyConstraint(
            ["organization_id", "port_id"],
            ["port.organization_id", "port.id"],
            name="fk_location_port",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_location_org_id"),
        sa.CheckConstraint(
            "kind IN ('unlocode', 'postal_zone', 'address')",
            name="ck_location_kind",
        ),
        sa.CheckConstraint(
            """
            CASE kind
              WHEN 'unlocode' THEN port_id IS NOT NULL
                AND city IS NULL AND address_line IS NULL AND postal_code IS NULL
              WHEN 'postal_zone' THEN code IS NOT NULL AND port_id IS NULL
              WHEN 'address' THEN country_code IS NOT NULL
                AND city IS NOT NULL AND address_line IS NOT NULL AND port_id IS NULL
            END
            """,
            name="ck_location_kind_shape",
        ),
    )
    op.create_index("ix_location_organization_id", "location", ["organization_id"])
    op.execute(
        "CREATE UNIQUE INDEX uq_location_org_code ON location (organization_id, code) "
        "WHERE code IS NOT NULL"
    )

    op.create_table(
        "location_zone_member",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("zone_location_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("postal_from", sa.Text(), nullable=False),
        sa.Column("postal_to", sa.Text(), nullable=False),
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
            name="fk_location_zone_member_organization_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id", "zone_location_id"],
            ["location.organization_id", "location.id"],
            name="fk_location_zone_member_zone",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "length(postal_from) = length(postal_to)",
            name="ck_location_zone_member_equal_length",
        ),
        # Porównanie bajtowe, bo zakres domyka się w kolacji "C", nie w PL/DE.
        sa.CheckConstraint(
            'postal_from COLLATE "C" <= postal_to COLLATE "C"',
            name="ck_location_zone_member_ordered",
        ),
    )
    op.create_index(
        "ix_location_zone_member_organization_id",
        "location_zone_member",
        ["organization_id"],
    )
    op.create_index(
        "ix_location_zone_member_zone_location_id",
        "location_zone_member",
        ["zone_location_id"],
    )
    op.execute(
        "ALTER TABLE location_zone_member ADD COLUMN postal_span postal_range "
        "GENERATED ALWAYS AS (postal_range(postal_from, postal_to, '[]')) STORED"
    )
    # organization_id WITH = jest konieczne: exclusion patrzy poza RLS, więc bez niego
    # zakres jednego tenanta blokowałby zapis drugiemu.
    op.execute(
        """
        ALTER TABLE location_zone_member ADD CONSTRAINT ex_zone_member_no_overlap
        EXCLUDE USING gist (
          organization_id WITH =, country_code WITH =, postal_span WITH &&
        )
        """
    )

    for table in ("location", "location_zone_member"):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(
            f"""
            CREATE POLICY {table}_tenant_isolation ON {table}
            USING (organization_id = {_ORG})
            WITH CHECK (organization_id = {_ORG})
            """
        )


def downgrade() -> None:
    for table in ("location_zone_member", "location"):
        op.execute(f"DROP POLICY IF EXISTS {table}_tenant_isolation ON {table}")

    op.drop_index("ix_location_zone_member_zone_location_id", table_name="location_zone_member")
    op.drop_index("ix_location_zone_member_organization_id", table_name="location_zone_member")
    op.drop_table("location_zone_member")

    op.execute("DROP INDEX IF EXISTS uq_location_org_code")
    op.drop_index("ix_location_organization_id", table_name="location")
    op.drop_table("location")

    op.execute("DROP TYPE IF EXISTS postal_range")
    op.drop_constraint("uq_port_org_id", "port", type_="unique")
    op.execute("DROP EXTENSION IF EXISTS btree_gist")
