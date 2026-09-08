from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.document_dispatch_rule import (
    require_dispatch_document_kind,
    require_dispatch_incoterm,
    require_dispatch_source_ref,
    require_dispatch_trade_side,
    require_recipient_role,
)
from app.models.document_dispatch_rule import DocumentDispatchRule
from app.repositories.document_dispatch_rules.document_dispatch_rule_repository import (
    DocumentDispatchRuleRepository,
)


class DocumentDispatchRuleService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = DocumentDispatchRuleRepository(session)

    async def list_for_pair(
        self,
        *,
        incoterm: object,
        trade_side: object,
        document_kind: object | None = None,
    ) -> list[DocumentDispatchRule]:
        code = require_dispatch_incoterm(incoterm)
        side = require_dispatch_trade_side(trade_side)
        if document_kind is None:
            return await self._rows.list_current_for_pair(code, side)
        kind = require_dispatch_document_kind(document_kind)
        found = await self._rows.find_current(code, side, kind)
        return [] if found is None else [found]

    async def record_rule(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incoterm: object,
        trade_side: object,
        document_kind: object,
        recipient_role: object,
        source_ref: object,
    ) -> DocumentDispatchRule:
        code = require_dispatch_incoterm(incoterm)
        side = require_dispatch_trade_side(trade_side)
        kind = require_dispatch_document_kind(document_kind)
        role = require_recipient_role(recipient_role)
        origin = require_dispatch_source_ref(source_ref)
        current = await self._rows.find_current(code, side, kind)
        if (
            current is not None
            and current.recipient_role == role
            and current.source_ref == origin
        ):
            return current
        saved = await self._rows.add(
            DocumentDispatchRule(
                id=uuid4(),
                organization_id=organization_id,
                incoterm=code,
                trade_side=side,
                document_kind=kind,
                recipient_role=role,
                source_ref=origin,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
