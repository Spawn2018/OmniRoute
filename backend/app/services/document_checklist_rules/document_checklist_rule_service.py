from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.document_checklist_rule import (
    require_blocks_dispatch,
    require_checklist_document_kind,
    require_checklist_incoterm,
    require_checklist_mode,
    require_checklist_trade_side,
)
from app.domain.errors import InvalidDocumentChecklistRule
from app.models.document_checklist_rule import DocumentChecklistRule
from app.repositories.document_checklist_rules.document_checklist_rule_repository import (
    DocumentChecklistRuleRepository,
)


class DocumentChecklistRuleService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = DocumentChecklistRuleRepository(session)

    async def list_for_triple(
        self,
        *,
        incoterm: object,
        trade_side: object,
        mode: object,
    ) -> list[DocumentChecklistRule]:
        return await self._rows.list_for_triple(
            require_checklist_incoterm(incoterm),
            require_checklist_trade_side(trade_side),
            require_checklist_mode(mode),
        )

    async def record_rule(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incoterm: object,
        trade_side: object,
        mode: object,
        document_kind: object,
        blocks_dispatch: object,
    ) -> DocumentChecklistRule:
        row = DocumentChecklistRule(
            id=uuid4(),
            organization_id=organization_id,
            incoterm=require_checklist_incoterm(incoterm),
            trade_side=require_checklist_trade_side(trade_side),
            mode=require_checklist_mode(mode),
            document_kind=require_checklist_document_kind(document_kind),
            blocks_dispatch=require_blocks_dispatch(blocks_dispatch),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidDocumentChecklistRule("reguła już zapisana") from orig
