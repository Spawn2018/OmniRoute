from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.webhook_outbox_mark import WebhookOutboxMark
from app.services.webhook_outbox_marks.webhook_outbox_mark_service import (
    WebhookOutboxMarkService,
)

router = APIRouter(prefix="/webhook-outbox-marks", tags=["webhook-outbox-marks"])

_PERM = "can_manage_webhook_outbox_marks"


class WebhookOutboxMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    outbox_kind: str
    source_ref: str


class WebhookOutboxMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    outbox_kind: str
    source_ref: str


def _row(saved: WebhookOutboxMark) -> WebhookOutboxMarkResponse:
    return WebhookOutboxMarkResponse.model_validate(saved)


@router.get("", response_model=list[WebhookOutboxMarkResponse])
async def list_webhook_outbox_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[WebhookOutboxMarkResponse]:
    packed = await WebhookOutboxMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=WebhookOutboxMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_webhook_outbox_mark(
    body: WebhookOutboxMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> WebhookOutboxMarkResponse:
    saved = await WebhookOutboxMarkService(session).persist_webhook_outbox_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        outbox_kind=body.outbox_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
