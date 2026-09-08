from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_dispatch_rule import DocumentDispatchRule


class DocumentDispatchRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current_for_pair(
        self,
        incoterm: str,
        trade_side: str,
    ) -> list[DocumentDispatchRule]:
        result = await self._session.scalars(
            select(DocumentDispatchRule)
            .where(
                DocumentDispatchRule.incoterm == incoterm,
                DocumentDispatchRule.trade_side == trade_side,
                DocumentDispatchRule.superseded_by.is_(None),
            )
            .order_by(
                DocumentDispatchRule.document_kind,
                DocumentDispatchRule.created_at.desc(),
                DocumentDispatchRule.id,
            ),
        )
        return list(result.all())

    async def find_current(
        self,
        incoterm: str,
        trade_side: str,
        document_kind: str,
    ) -> DocumentDispatchRule | None:
        result = await self._session.scalars(
            select(DocumentDispatchRule)
            .where(
                DocumentDispatchRule.incoterm == incoterm,
                DocumentDispatchRule.trade_side == trade_side,
                DocumentDispatchRule.document_kind == document_kind,
                DocumentDispatchRule.superseded_by.is_(None),
            )
            .order_by(DocumentDispatchRule.created_at.desc(), DocumentDispatchRule.id),
        )
        return result.first()

    async def add(self, row: DocumentDispatchRule) -> DocumentDispatchRule:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(
        self,
        current: DocumentDispatchRule,
        successor_id: UUID,
    ) -> DocumentDispatchRule:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
