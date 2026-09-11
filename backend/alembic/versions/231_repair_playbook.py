"""create repair_playbook catalog with RLS FORCE

Revision ID: 231_repair_playbook
Revises: 230_calibration_mark
Create Date: 2026-09-11

CI8 HITL playbook naprawy jako dane. Nie auto-send. Nie kwota.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "231_repair_playbook"
down_revision: str | None = "230_calibration_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    op.create_table(
        "repair_playbook",
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("playbook_code", sa.String(length=32), nullable=False),
        sa.Column("stance_kind", sa.String(length=16), nullable=False),
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
            name="fk_repair_playbook_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("organization_id", "id", name="uq_repair_playbook_org_id"),
        sa.UniqueConstraint(
            "organization_id",
            "playbook_code",
            name="uq_repair_playbook_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_repair_playbook_org_source_ref",
        ),
        sa.CheckConstraint(
            "playbook_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_repair_playbook_code",
        ),
        sa.CheckConstraint(
            "stance_kind IN ('contain', 'reroute', 'claim', 'other')",
            name="ck_repair_playbook_stance_kind",
        ),
    )
    op.create_index(
        "ix_repair_playbook_organization_id",
        "repair_playbook",
        ["organization_id"],
    )
    op.execute("ALTER TABLE repair_playbook ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE repair_playbook FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY repair_playbook_tenant_isolation ON repair_playbook
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS repair_playbook_tenant_isolation ON repair_playbook"
    )
    op.drop_index(
        "ix_repair_playbook_organization_id",
        table_name="repair_playbook",
    )
    op.drop_table("repair_playbook")
