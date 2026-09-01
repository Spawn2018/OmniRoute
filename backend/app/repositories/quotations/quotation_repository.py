from uuid import UUID, uuid4

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quotation import Quotation

QUOTE_FROM_CURRENT_SQL = """
INSERT INTO quotation (
    id, organization_id, charge_code, rate_line_id,
    amount, currency, source_ref, created_by
)
SELECT
    :qid,
    :org,
    rl.charge_code,
    rl.id,
    rl.amount,
    rl.currency,
    rl.source_ref,
    :created_by
FROM rate_line AS rl
WHERE rl.charge_code = :charge_code
  AND rl.superseded_by IS NULL
ORDER BY rl.created_at DESC, rl.id
LIMIT 1
RETURNING id, organization_id, charge_code, rate_line_id,
          amount, currency, source_ref, created_by
"""


class QuotationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Quotation]:
        result = await self._session.scalars(
            select(Quotation).order_by(Quotation.created_at.desc(), Quotation.id),
        )
        return list(result.all())

    async def insert_from_current_rate(
        self,
        *,
        organization_id: UUID,
        created_by: UUID,
        charge_code: str,
    ) -> Quotation | None:
        result = await self._session.execute(
            text(QUOTE_FROM_CURRENT_SQL),
            {
                "qid": uuid4(),
                "org": organization_id,
                "created_by": created_by,
                "charge_code": charge_code,
            },
        )
        row = result.mappings().first()
        if row is None:
            return None
        return Quotation(
            id=row["id"],
            organization_id=row["organization_id"],
            charge_code=row["charge_code"],
            rate_line_id=row["rate_line_id"],
            amount=row["amount"],
            currency=row["currency"],
            source_ref=row["source_ref"],
            created_by=row["created_by"],
        )
