from uuid import UUID, uuid4

from sqlalchemy import select, text
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quotation import Quotation

QUOTE_FROM_CURRENT_SQL = """
INSERT INTO quotation (
    id, organization_id, charge_code, rate_line_id,
    amount, currency, source_ref, created_by,
    origin_port_id, destination_port_id, party_id, customer_rfq_id,
    commodity_code_id
)
SELECT
    :qid,
    :org,
    rl.charge_code,
    rl.id,
    rl.amount,
    rl.currency,
    rl.source_ref,
    :created_by,
    :origin_port_id,
    :destination_port_id,
    :party_id,
    :customer_rfq_id,
    :commodity_code_id
FROM rate_line AS rl
WHERE rl.charge_code = :charge_code
  AND rl.superseded_by IS NULL
ORDER BY rl.created_at DESC, rl.id
LIMIT 1
RETURNING id, organization_id, charge_code, rate_line_id,
          amount, currency, source_ref, created_by,
          origin_port_id, destination_port_id, party_id, customer_rfq_id,
          commodity_code_id, document_number
"""

ISSUE_DOCUMENT_NUMBER_SQL = """
UPDATE quotation AS target
SET document_number = :prefix || LPAD(nxt.seq::text, 4, '0')
FROM (
    SELECT COALESCE(
        MAX(
            CAST(
                SUBSTRING(document_number FROM (LENGTH(:prefix) + 1)) AS INTEGER
            )
        ),
        0
    ) + 1 AS seq
    FROM quotation
    WHERE document_number IS NOT NULL
      AND LENGTH(document_number) = LENGTH(:prefix) + 4
      AND document_number LIKE :prefix || '%'
) AS nxt
WHERE target.id = :qid
  AND target.document_number IS NULL
RETURNING target.id, target.organization_id, target.charge_code, target.rate_line_id,
          target.amount, target.currency, target.source_ref, target.created_by,
          target.origin_port_id, target.destination_port_id, target.party_id,
          target.customer_rfq_id, target.commodity_code_id, target.document_number
"""


def quotation_from_insert_row(row: RowMapping) -> Quotation:
    return Quotation(
        id=row["id"],
        organization_id=row["organization_id"],
        charge_code=row["charge_code"],
        rate_line_id=row["rate_line_id"],
        amount=row["amount"],
        currency=row["currency"],
        source_ref=row["source_ref"],
        created_by=row["created_by"],
        origin_port_id=row["origin_port_id"],
        destination_port_id=row["destination_port_id"],
        party_id=row["party_id"],
        customer_rfq_id=row.get("customer_rfq_id"),
        commodity_code_id=row.get("commodity_code_id"),
        document_number=row.get("document_number"),
        negotiated_channel_quote_id=row.get("negotiated_channel_quote_id"),
        noted_credit_review_id=row.get("noted_credit_review_id"),
    )


class QuotationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(
        self,
        *,
        party_id: UUID | None = None,
        origin_port_id: UUID | None = None,
        destination_port_id: UUID | None = None,
        customer_rfq_id: UUID | None = None,
    ) -> list[Quotation]:
        stmt = select(Quotation)
        if party_id is not None:
            stmt = stmt.where(Quotation.party_id == party_id)
        if origin_port_id is not None:
            stmt = stmt.where(Quotation.origin_port_id == origin_port_id)
        if destination_port_id is not None:
            stmt = stmt.where(Quotation.destination_port_id == destination_port_id)
        if customer_rfq_id is not None:
            stmt = stmt.where(Quotation.customer_rfq_id == customer_rfq_id)
        stmt = stmt.order_by(Quotation.created_at.desc(), Quotation.id)
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def insert_from_current_rate(
        self,
        *,
        organization_id: UUID,
        created_by: UUID,
        charge_code: str,
        origin_port_id: UUID,
        destination_port_id: UUID,
        party_id: UUID,
        customer_rfq_id: UUID | None = None,
        commodity_code_id: UUID | None = None,
    ) -> Quotation | None:
        result = await self._session.execute(
            text(QUOTE_FROM_CURRENT_SQL),
            {
                "qid": uuid4(),
                "org": organization_id,
                "created_by": created_by,
                "charge_code": charge_code,
                "origin_port_id": origin_port_id,
                "destination_port_id": destination_port_id,
                "party_id": party_id,
                "customer_rfq_id": customer_rfq_id,
                "commodity_code_id": commodity_code_id,
            },
        )
        row = result.mappings().first()
        if row is None:
            return None
        return quotation_from_insert_row(row)

    async def get(self, quotation_id: UUID) -> Quotation | None:
        found = await self._session.get(Quotation, quotation_id, populate_existing=True)
        return found if isinstance(found, Quotation) else None

    async def save(self, row: Quotation) -> Quotation:
        await self._session.flush()
        return row

    async def issue_document_number(
        self,
        *,
        quotation_id: UUID,
        prefix: str,
    ) -> Quotation | None:
        result = await self._session.execute(
            text(ISSUE_DOCUMENT_NUMBER_SQL),
            {"qid": quotation_id, "prefix": prefix},
        )
        row = result.mappings().first()
        if row is None:
            return None
        cached = await self._session.get(Quotation, quotation_id)
        if cached is None:
            return quotation_from_insert_row(row)
        cached.document_number = row["document_number"]
        return cached
