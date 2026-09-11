from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.aeo_dossier_mark import AeoDossierMark
from app.services.aeo_dossier_marks.aeo_dossier_mark_service import AeoDossierMarkService

router = APIRouter(prefix="/aeo-dossier-marks", tags=["aeo-dossier-marks"])

_PERM = "can_manage_aeo_dossier_marks"


class AeoDossierMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    dossier_kind: str
    source_ref: str


class AeoDossierMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    dossier_kind: str
    source_ref: str


def _row(saved: AeoDossierMark) -> AeoDossierMarkResponse:
    return AeoDossierMarkResponse.model_validate(saved)


@router.get("", response_model=list[AeoDossierMarkResponse])
async def list_aeo_dossier_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AeoDossierMarkResponse]:
    packed = await AeoDossierMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=AeoDossierMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_aeo_dossier_mark(
    body: AeoDossierMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AeoDossierMarkResponse:
    saved = await AeoDossierMarkService(session).persist_aeo_dossier_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        dossier_kind=body.dossier_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
