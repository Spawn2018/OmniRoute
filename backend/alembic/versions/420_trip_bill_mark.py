"""create trip_bill_mark catalog with RLS FORCE

Revision ID: 420_trip_bill_mark
Revises: 419_handover_sbar_mark
Create Date: 2026-09-16

N2 HITL gotowość przejazdu do FV. Nie widok SQL na charge. Nie KSeF HTTP.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "420_trip_bill_mark"
down_revision: str | None = "419_handover_sbar_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "trip_bill_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("bill_kind", sa.String(length=16), nullable=False),
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
            name="fk_trip_bill_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "id",
            name="uq_trip_bill_mark_org_id",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_trip_bill_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_trip_bill_mark_org_src",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_trip_bill_mark_code",
        ),
        sa.CheckConstraint(
            "bill_kind IN ("
            "'ready', 'held', 'billed', 'other'"
            ")",
            name="ck_trip_bill_mark_kind",
        ),
    )
    op.create_index(
        "ix_trip_bill_mark_organization_id",
        "trip_bill_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE trip_bill_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE trip_bill_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY trip_bill_mark_tenant_isolation
        ON trip_bill_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS trip_bill_mark_tenant_isolation ON trip_bill_mark",
    )
    op.drop_index(
        "ix_trip_bill_mark_organization_id",
        table_name="trip_bill_mark",
    )
    op.drop_table("trip_bill_mark")
