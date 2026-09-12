"""create eur1_atr_mark catalog with RLS FORCE

Revision ID: 271_eur1_atr_mark
Revises: 276_MQC_mark
Create Date: 2026-09-12

EXP3.7 HITL znacznik MQC jako dane. Nie live giełda. Nie ATR scrape.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "283_eur1_atr_mark"
down_revision: str | None = "282_eccn_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "eur1_atr_mark",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("cert_kind", sa.String(length=16), nullable=False),
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
            name="fk_eur1_atr_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_eur1_atr_mark_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_eur1_atr_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_eur1_atr_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_eur1_atr_mark_code",
        ),
        sa.CheckConstraint(
            "cert_kind IN ('eur1', 'atr', 'origin', 'other')",
            name="ck_eur1_atr_mark_cert_kind",
        ),
    )
    op.create_index(
        "ix_eur1_atr_mark_organization_id",
        "eur1_atr_mark",
        ["organization_id"],
    )
    op.execute("ALTER TABLE eur1_atr_mark ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE eur1_atr_mark FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY eur1_atr_mark_tenant_isolation ON eur1_atr_mark
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS eur1_atr_mark_tenant_isolation ON eur1_atr_mark",
    )
    op.drop_index(
        "ix_eur1_atr_mark_organization_id",
        table_name="eur1_atr_mark",
    )
    op.drop_table("eur1_atr_mark")
