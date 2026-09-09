from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.kreptd_licence import KreptdLicence
from app.services.kreptd_licences.kreptd_licence_service import KreptdLicenceService
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/kreptd-licences", tags=["kreptd-licences"])

_PERM = "can_manage_kreptd_licences"


class KreptdLicenceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    licence_no: str
    source_ref: str


class KreptdLicenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    licence_no: str
    source_ref: str


def _as_row(row: KreptdLicence) -> KreptdLicenceResponse:
    return KreptdLicenceResponse(
        id=row.id,
        organization_id=row.organization_id,
        party_id=row.party_id,
        licence_no=row.licence_no,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[KreptdLicenceResponse])
async def list_kreptd_licences(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[KreptdLicenceResponse]:
    rows = await KreptdLicenceService(session).list_licences()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=KreptdLicenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_kreptd_licence(
    body: KreptdLicenceCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> KreptdLicenceResponse:
    party = await PartyService(session).get_party(body.party_id)
    row = await KreptdLicenceService(session).persist_licence(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party.id,
        licence_no=body.licence_no,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
