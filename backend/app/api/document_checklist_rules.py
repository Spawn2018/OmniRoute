from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.document_checklist_rule import DocumentChecklistRule
from app.services.document_checklist_rules.document_checklist_rule_service import (
    DocumentChecklistRuleService,
)

router = APIRouter(prefix="/document-checklist-rules", tags=["document-checklist-rules"])


class DocumentChecklistRuleCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incoterm: str
    trade_side: str
    mode: str
    document_kind: str
    blocks_dispatch: bool


class DocumentChecklistRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    incoterm: str
    trade_side: str
    mode: str
    document_kind: str
    blocks_dispatch: bool

    @classmethod
    def from_row(cls, row: DocumentChecklistRule) -> "DocumentChecklistRuleResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            incoterm=str(row.incoterm).strip(),
            trade_side=row.trade_side,
            mode=row.mode,
            document_kind=row.document_kind,
            blocks_dispatch=row.blocks_dispatch,
        )


@router.get("", response_model=list[DocumentChecklistRuleResponse])
async def list_document_checklist_rules(
    incoterm: str = Query(...),
    trade_side: str = Query(...),
    mode: str = Query(...),
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DocumentChecklistRuleResponse]:
    rows = await DocumentChecklistRuleService(session).list_for_triple(
        incoterm=incoterm,
        trade_side=trade_side,
        mode=mode,
    )
    return [DocumentChecklistRuleResponse.from_row(row) for row in rows]


@router.post(
    "",
    response_model=DocumentChecklistRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_checklist_rule(
    body: DocumentChecklistRuleCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DocumentChecklistRuleResponse:
    row = await DocumentChecklistRuleService(session).record_rule(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        incoterm=body.incoterm,
        trade_side=body.trade_side,
        mode=body.mode,
        document_kind=body.document_kind,
        blocks_dispatch=body.blocks_dispatch,
    )
    await session.commit()
    return DocumentChecklistRuleResponse.from_row(row)
