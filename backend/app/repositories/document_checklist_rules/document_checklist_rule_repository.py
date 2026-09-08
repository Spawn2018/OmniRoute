from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_checklist_rule import DocumentChecklistRule


class DocumentChecklistRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_triple(
        self,
        incoterm: str,
        trade_side: str,
        mode: str,
    ) -> list[DocumentChecklistRule]:
        result = await self._session.scalars(
            select(DocumentChecklistRule)
            .where(
                DocumentChecklistRule.incoterm == incoterm,
                DocumentChecklistRule.trade_side == trade_side,
                DocumentChecklistRule.mode == mode,
            )
            .order_by(DocumentChecklistRule.created_at.desc(), DocumentChecklistRule.id),
        )
        return list(result.all())

    async def add(self, row: DocumentChecklistRule) -> DocumentChecklistRule:
        self._session.add(row)
        await self._session.flush()
        return row
