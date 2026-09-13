"""create tracking_consent catalog with RLS FORCE

Revision ID: 364_tracking_consent
Revises: 363_telematics_device
Create Date: 2026-09-13

BR2.2 HITL katalog zgody. Nie kolumna na kontakcie. Nie poll.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "364_tracking_consent"
down_revision: str | None = "363_telematics_device"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "tracking_consent",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("consent_code", sa.String(length=32), nullable=False),
        sa.Column("consent_kind", sa.String(length=16), nullable=False),
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
            name="fk_tracking_consent_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_tracking_consent_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "consent_code",
            name="uq_tracking_consent_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tracking_consent_org_source_ref",
        ),
        sa.CheckConstraint(
            "consent_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tracking_consent_code",
        ),
        sa.CheckConstraint(
            "consent_kind IN ('party', 'driver', 'other')",
            name="ck_tracking_consent_kind",
        ),
    )
    op.create_index(
        "ix_tracking_consent_organization_id",
        "tracking_consent",
        ["organization_id"],
    )
    op.execute("ALTER TABLE tracking_consent ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tracking_consent FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tracking_consent_tenant_isolation ON tracking_consent
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS tracking_consent_tenant_isolation ON tracking_consent",
    )
    op.drop_index(
        "ix_tracking_consent_organization_id",
        table_name="tracking_consent",
    )
    op.drop_table("tracking_consent")
