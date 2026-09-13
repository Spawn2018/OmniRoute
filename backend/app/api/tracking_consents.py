from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tracking_consent import TrackingConsent
from app.services.tracking_consents.tracking_consent_service import TrackingConsentService

router = APIRouter(prefix="/tracking-consents", tags=["tracking-consents"])

_PERM = "can_manage_tracking_consents"


class TrackingConsentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    consent_code: str
    consent_kind: str
    source_ref: str


class TrackingConsentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    consent_code: str
    consent_kind: str
    source_ref: str


def _row(saved: TrackingConsent) -> TrackingConsentResponse:
    return TrackingConsentResponse.model_validate(saved)


@router.get("", response_model=list[TrackingConsentResponse])
async def list_tracking_consents(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TrackingConsentResponse]:
    packed = await TrackingConsentService(session).list_consents()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=TrackingConsentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tracking_consent(
    body: TrackingConsentCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TrackingConsentResponse:
    saved = await TrackingConsentService(session).persist_tracking_consent(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        consent_code=body.consent_code,
        consent_kind=body.consent_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
