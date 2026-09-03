from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.errors import ResourceNotFound
from app.domain.gdpr_request import ERASED_DISPLAY_NAME, erasure_mailbox
from app.models.gdpr_request import GdprRequest
from app.services.gdpr_requests.gdpr_request_service import GdprRequestService
from app.services.tenancy.service import TenancyService

router = APIRouter(prefix="/gdpr-requests", tags=["gdpr-requests"])


class GdprRequestCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    app_user_id: UUID
    request_kind: str
    source_ref: str


class GdprRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    app_user_id: UUID
    request_kind: str
    status: str
    source_ref: str


@router.get("", response_model=list[GdprRequestResponse])
async def list_gdpr_requests(
    _authz: None = Depends(require_permission("can_manage_gdpr_requests", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[GdprRequestResponse]:
    rows = await GdprRequestService(session).list_rows()
    return [GdprRequestResponse.model_validate(row) for row in rows]


@router.post("", response_model=GdprRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_gdpr_request(
    body: GdprRequestCreate,
    _authz: None = Depends(require_permission("can_manage_gdpr_requests", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> GdprRequestResponse:
    subject = await TenancyService(session).get_user(body.app_user_id)
    if subject is None:
        raise ResourceNotFound("nieznane konto")
    row = await GdprRequestService(session).record_row(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        app_user_id=subject.id,
        request_kind=body.request_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return GdprRequestResponse.model_validate(row)


@router.post("/{request_id}/fulfill", response_model=GdprRequestResponse)
async def fulfill_gdpr_request(
    request_id: UUID,
    _authz: None = Depends(require_permission("can_manage_gdpr_requests", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> GdprRequestResponse:
    row = await GdprRequestService(session).fulfill(request_id)
    await _erase_directory_if_needed(session, row)
    await session.commit()
    return GdprRequestResponse.model_validate(row)


async def _erase_directory_if_needed(session: AsyncSession, row: GdprRequest) -> None:
    if row.request_kind != "erasure":
        return
    erased = await TenancyService(session).erase_directory_subject(
        row.app_user_id,
        email=erasure_mailbox(row.app_user_id),
        display_name=ERASED_DISPLAY_NAME,
    )
    if erased is None:
        raise ResourceNotFound("nieznane konto")
