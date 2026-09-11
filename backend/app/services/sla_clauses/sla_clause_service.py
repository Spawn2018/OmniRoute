from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.sla_clause import parse_sla_clause_row
from app.models.sla_clause import SlaClause
from app.repositories.sla_clauses.sla_clause_repository import SlaClauseRepository


class SlaClauseService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SlaClauseRepository(session)

    async def list_clauses(self) -> list[SlaClause]:
        return await self._rows.list_clauses()

    async def persist_sla_clause(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        customer_contract_id: object,
        clause_code: object,
        metric_kind: object,
        threshold_label: object,
        source_ref: object,
    ) -> SlaClause:
        packed = parse_sla_clause_row(
            customer_contract_id=customer_contract_id,
            clause_code=clause_code,
            metric_kind=metric_kind,
            threshold_label=threshold_label,
            source_ref=source_ref,
        )
        header = await self._rows.get_contract(packed[0])
        if header is None:
            raise ResourceNotFound("nieznana umowa")
        row = SlaClause(
            id=uuid4(),
            organization_id=organization_id,
            customer_contract_id=packed[0],
            clause_code=packed[1],
            metric_kind=packed[2],
            threshold_label=packed[3],
            source_ref=packed[4],
            created_by=user_id,
        )
        return await self._rows.add_clause(row)
