"""create blank_sailing_mark catalog with RLS FORCE

Revision ID: 445_blank_sailing_mark
Revises: 444_shipment_is_waste
Create Date: 2026-09-18

V3 HITL blank_sailing_mark. Nie countdown N3. Nie szkic charge.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "445_blank_sailing_mark"
down_revision: str | None = "444_shipment_is_waste"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "blank_sailing_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("sailing_kind", sa.String(length=16), nullable=False),
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
            name="fk_blank_sailing_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_blank_sailing_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_blank_sailing_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_blank_sailing_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_blank_sailing_mark_code",
        ),
        sa.CheckConstraint(
            "sailing_kind IN ('blank', 'congestion', 'gate', 'other')",
            name="ck_blank_sailing_mark_sailing_kind",
        ),
    )
    op.create_index(
        "ix_blank_sailing_mark_organization_id",
        "blank_sailing_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE blank_sailing_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE blank_sailing_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY blank_sailing_mark_tenant_isolation
        ON blank_sailing_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS blank_sailing_mark_tenant_isolation ON blank_sailing_mark"
    )
    op.drop_index(
        "ix_blank_sailing_mark_organization_id",
        table_name="blank_sailing_mark",
    )
    op.drop_table("blank_sailing_mark")
