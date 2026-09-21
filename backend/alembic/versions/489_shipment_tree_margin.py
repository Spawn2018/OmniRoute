"""read-only margin of a shipment root plus its direct children

Revision ID: 489_shipment_tree_margin
Revises: 488_charge_shipment_id
Create Date: 2026-09-21

Widok, nie magazyn marży. Suma zostaje w Postgres (HC-11).
security_invoker: RLS wołającego na shipment i charge.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "489_shipment_tree_margin"
down_revision: str | None = "488_charge_shipment_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_VIEW = """
CREATE VIEW shipment_tree_margin
WITH (security_invoker = true) AS
SELECT
  root.organization_id,
  root.id AS shipment_id,
  c.buy_currency AS currency,
  sum(c.buy_amount) AS buy_amount,
  sum(c.sell_amount) AS sell_amount,
  sum(c.sell_amount - c.buy_amount) AS margin_amount,
  count(c.id)::bigint AS charge_count
FROM shipment AS root
JOIN shipment AS node
  ON node.organization_id = root.organization_id
 AND (node.id = root.id OR node.parent_shipment_id = root.id)
JOIN charge AS c
  ON c.organization_id = node.organization_id
 AND c.shipment_id = node.id
WHERE root.parent_shipment_id IS NULL
GROUP BY root.organization_id, root.id, c.buy_currency
"""


def upgrade() -> None:
    op.execute(_VIEW)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS shipment_tree_margin")
