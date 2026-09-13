"""create shipper_tender_mark catalog with RLS FORCE

Revision ID: 366_shipper_tender_mk
Revises: 365_sales_lane
Create Date: 2026-09-13

BR6.2 HITL katalog trybu zaladowcy. Nie druga tabela tender. Nie Alpega.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "366_shipper_tender_mk"
down_revision: str | None = "365_sales_lane"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "shipper_tender_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("shipper_kind", sa.String(length=16), nullable=False),
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
            name="fk_shipper_tender_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_shipper_tender_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_shipper_tender_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_shipper_tender_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipper_tender_mark_code",
        ),
        sa.CheckConstraint(
            "shipper_kind IN ('round', 'bench', 'spot', 'other')",
            name="ck_shipper_tender_mark_kind",
        ),
    )
    op.create_index(
        "ix_shipper_tender_mark_organization_id",
        "shipper_tender_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE shipper_tender_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE shipper_tender_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY shipper_tender_mark_tenant_isolation ON shipper_tender_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS shipper_tender_mark_tenant_isolation ON shipper_tender_mark",
    )
    op.drop_index(
        "ix_shipper_tender_mark_organization_id",
        table_name="shipper_tender_mark",
    )
    op.drop_table("shipper_tender_mark")
