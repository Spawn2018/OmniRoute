from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.document_dispatch_rule import DocumentDispatchRule
from app.services.document_dispatch_rules.document_dispatch_rule_service import (
    DocumentDispatchRuleService,
)

router = APIRouter(prefix="/document-dispatch-rules", tags=["document-dispatch-rules"])


class DocumentDispatchRuleCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incoterm: str
    trade_side: str
    document_kind: str
    recipient_role: str
    source_ref: str


class DocumentDispatchRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    incoterm: str
    trade_side: str
    document_kind: str
    recipient_role: str
    source_ref: str
    superseded_by: UUID | None

    @classmethod
    def from_row(cls, row: DocumentDispatchRule) -> "DocumentDispatchRuleResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            incoterm=str(row.incoterm).strip(),
            trade_side=row.trade_side,
            document_kind=row.document_kind,
            recipient_role=row.recipient_role,
            source_ref=row.source_ref,
            superseded_by=row.superseded_by,
        )


@router.get("", response_model=list[DocumentDispatchRuleResponse])
async def list_document_dispatch_rules(
    incoterm: str = Query(...),
    trade_side: str = Query(...),
    document_kind: str | None = Query(default=None),
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DocumentDispatchRuleResponse]:
    kind = None if document_kind is None or document_kind.strip() == "" else document_kind
    rows = await DocumentDispatchRuleService(session).list_for_pair(
        incoterm=incoterm,
        trade_side=trade_side,
        document_kind=kind,
    )
    return [DocumentDispatchRuleResponse.from_row(row) for row in rows]


@router.post(
    "",
    response_model=DocumentDispatchRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_dispatch_rule(
    body: DocumentDispatchRuleCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DocumentDispatchRuleResponse:
    row = await DocumentDispatchRuleService(session).record_rule(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        incoterm=body.incoterm,
        trade_side=body.trade_side,
        document_kind=body.document_kind,
        recipient_role=body.recipient_role,
        source_ref=body.source_ref,
    )
    await session.commit()
    return DocumentDispatchRuleResponse.from_row(row)
