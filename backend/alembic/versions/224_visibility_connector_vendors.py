"""expand visibility_connector system_kind to fourkites/shippeo

Revision ID: 224_visibility_connector_vendors
Revises: 223_shipment_asn_id
Create Date: 2026-09-11

CT7 HITL: tokeny FourKites/Shippeo obok p44. Nie live HTTP.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "224_visibility_connector_vendors"
down_revision: str | None = "223_shipment_asn_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_KIND_SQL = "system_kind IN ('p44', 'fourkites', 'shippeo')"
_KIND_P44 = "system_kind IN ('p44')"


def upgrade() -> None:
    op.drop_constraint("ck_visibility_connector_kind", "visibility_connector", type_="check")
    op.create_check_constraint(
        "ck_visibility_connector_kind",
        "visibility_connector",
        _KIND_SQL,
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM visibility_connector WHERE system_kind IN ('fourkites', 'shippeo')"
    )
    op.drop_constraint("ck_visibility_connector_kind", "visibility_connector", type_="check")
    op.create_check_constraint(
        "ck_visibility_connector_kind",
        "visibility_connector",
        _KIND_P44,
    )
