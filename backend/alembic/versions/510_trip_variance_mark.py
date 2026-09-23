"""create trip_variance_mark catalog with RLS FORCE

Revision ID: 510_trip_variance_mark
Revises: 509_handover_bind_mark
Create Date: 2026-09-23

Leftover N11 HITL stance wariancji przejazdu zmiany. Nie SQL na charge / druga marĹĽa.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "510_trip_variance_mark"
down_revision: str | None = "509_handover_bind_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "trip_variance_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("variance_kind", sa.String(length=32), nullable=False),
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
            name="fk_trip_variance_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id", "id", name="uq_trip_variance_mark_org_id"
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_trip_variance_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_trip_variance_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_trip_variance_mark_code",
        ),
        sa.CheckConstraint(
            "variance_kind IN ('expected', 'actual', 'gap', 'other')",
            name="ck_trip_variance_mark_kind",
        ),
    )
    op.create_index(
        "ix_trip_variance_mark_organization_id",
        "trip_variance_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE trip_variance_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE trip_variance_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY trip_variance_mark_tenant_isolation
        ON trip_variance_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS trip_variance_mark_tenant_isolation "
        "ON trip_variance_mark",
    )
    op.drop_index(
        "ix_trip_variance_mark_organization_id",
        table_name="trip_variance_mark",
    )
    op.drop_table("trip_variance_mark")
