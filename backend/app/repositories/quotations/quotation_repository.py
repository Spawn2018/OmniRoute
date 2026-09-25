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
    commodity_code_id, dangerous_good_id,
    incoterm, incoterms_version, trade_side, named_place,
    valid_until, revision_no, mqc_teu, mqc_window
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
    :commodity_code_id,
    :dangerous_good_id,
    :incoterm,
    :incoterms_version,
    :trade_side,
    :named_place,
    :valid_until,
    :revision_no,
    :mqc_teu,
    :mqc_window
FROM rate_line AS rl
WHERE rl.charge_code = :charge_code
  AND rl.superseded_by IS NULL
ORDER BY rl.created_at DESC, rl.id
LIMIT 1
RETURNING id, organization_id, charge_code, rate_line_id,
          amount, currency, source_ref, created_by,
          origin_port_id, destination_port_id, party_id, customer_rfq_id,
          commodity_code_id, dangerous_good_id, document_number,
          incoterm, incoterms_version, trade_side, named_place,
          valid_until, revision_no, mqc_teu, mqc_window
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
          target.customer_rfq_id, target.commodity_code_id, target.dangerous_good_id,
          target.document_number
"""


def _quote_insert_binds(
    *,
    organization_id: UUID,
    created_by: UUID,
    charge_code: str,
    origin_port_id: UUID,
    destination_port_id: UUID,
    party_id: UUID,
    customer_rfq_id: UUID | None,
    commodity_code_id: UUID | None,
    dangerous_good_id: UUID | None,
    incoterm: str | None,
    incoterms_version: str | None,
    trade_side: str | None,
    named_place: str | None,
    valid_until: object,
    revision_no: object,
    mqc_teu: object,
    mqc_window: object,
) -> dict[str, object]:
    return {
        "qid": uuid4(),
        "org": organization_id,
        "created_by": created_by,
        "charge_code": charge_code,
        "origin_port_id": origin_port_id,
        "destination_port_id": destination_port_id,
        "party_id": party_id,
        "customer_rfq_id": customer_rfq_id,
        "commodity_code_id": commodity_code_id,
        "dangerous_good_id": dangerous_good_id,
        "incoterm": incoterm,
        "incoterms_version": incoterms_version,
        "trade_side": trade_side,
        "named_place": named_place,
        "valid_until": valid_until,
        "revision_no": revision_no,
        "mqc_teu": mqc_teu,
        "mqc_window": mqc_window,
    }


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
        dangerous_good_id=row.get("dangerous_good_id"),
        document_number=row.get("document_number"),
        negotiated_channel_quote_id=row.get("negotiated_channel_quote_id"),
        noted_credit_review_id=row.get("noted_credit_review_id"),
        incoterm=row.get("incoterm"),
        incoterms_version=row.get("incoterms_version"),
        trade_side=row.get("trade_side"),
        named_place=row.get("named_place"),
        valid_until=row.get("valid_until"),
        revision_no=row.get("revision_no"),
        mqc_teu=row.get("mqc_teu"),
        mqc_window=row.get("mqc_window"),
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
        self, *, organization_id: UUID, created_by: UUID, charge_code: str,
        origin_port_id: UUID, destination_port_id: UUID, party_id: UUID,
        customer_rfq_id: UUID | None = None, commodity_code_id: UUID | None = None,
        dangerous_good_id: UUID | None = None, incoterm: str | None = None,
        incoterms_version: str | None = None, trade_side: str | None = None,
        named_place: str | None = None, valid_until: object = None,
        revision_no: object = None, mqc_teu: object = None, mqc_window: object = None,
    ) -> Quotation | None:
        result = await self._session.execute(
            text(QUOTE_FROM_CURRENT_SQL),
            _quote_insert_binds(
                organization_id=organization_id, created_by=created_by,
                charge_code=charge_code, origin_port_id=origin_port_id,
                destination_port_id=destination_port_id, party_id=party_id,
                customer_rfq_id=customer_rfq_id, commodity_code_id=commodity_code_id,
                dangerous_good_id=dangerous_good_id, incoterm=incoterm,
                incoterms_version=incoterms_version, trade_side=trade_side,
                named_place=named_place, valid_until=valid_until,
                revision_no=revision_no, mqc_teu=mqc_teu, mqc_window=mqc_window,
            ),
        )
        row = result.mappings().first()
        return None if row is None else quotation_from_insert_row(row)

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
