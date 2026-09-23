"""create local_charge_match_mark catalog with RLS FORCE

Revision ID: 512_local_charge_match_mark
Revises: 511_margin_match_mark
Create Date: 2026-09-23

Leftover P4c HITL stance dopłaty lokalnej.
Nie matching SQL vs local_charge. Nie warning-jako-fakt.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID as PGUUID

revision: str = "512_local_charge_match_mark"
down_revision: str | None = "511_margin_match_mark"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"
_TABLE = "local_charge_match_mark"


def _table_columns() -> list[sa.Column]:
    return [
        sa.Column("id", PGUUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", PGUUID(as_uuid=True), nullable=False),
        sa.Column("mark_code", sa.String(length=32), nullable=False),
        sa.Column("match_kind", sa.String(length=32), nullable=False),
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
    ]


def _table_constraints() -> list[sa.SchemaItem]:
    return [
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            name="fk_local_charge_match_mark_organization_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint(
            "organization_id", "id", name="uq_local_charge_match_mark_org_id"
        ),
        sa.UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_local_charge_match_mark_org_code",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_local_charge_match_mark_org_source_ref",
        ),
        sa.CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_local_charge_match_mark_code",
        ),
        sa.CheckConstraint(
            "match_kind IN ('match', 'gap', 'waive', 'other')",
            name="ck_local_charge_match_mark_kind",
        ),
    ]


def _enable_tenant_rls() -> None:
    op.create_index(
        "ix_local_charge_match_mark_organization_id",
        _TABLE,
        ["organization_id"],
    )
    op.execute(f"ALTER TABLE {_TABLE} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {_TABLE} FORCE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY local_charge_match_mark_tenant_isolation
        ON {_TABLE}
        USING (organization_id = {_ORG})
        WITH CHECK (organization_id = {_ORG})
        """
    )


def upgrade() -> None:
    op.create_table(_TABLE, *_table_columns(), *_table_constraints())
    _enable_tenant_rls()


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS local_charge_match_mark_tenant_isolation "
        f"ON {_TABLE}",
    )
    op.drop_index(
        "ix_local_charge_match_mark_organization_id",
        table_name=_TABLE,
    )
    op.drop_table(_TABLE)
