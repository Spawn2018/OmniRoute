from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ais_import_mark import AisImportMark
from app.services.ais_import_marks.ais_import_mark_service import AisImportMarkService

router = APIRouter(
    prefix="/ais-import-marks",
    tags=["ais-import-marks"],
)

_PERM = "can_manage_ais_import_marks"


class AisImportMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    import_kind: str
    source_ref: str


class AisImportMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    import_kind: str
    source_ref: str


def _row(saved: AisImportMark) -> AisImportMarkResponse:
    return AisImportMarkResponse.model_validate(saved)


@router.get("", response_model=list[AisImportMarkResponse])
async def list_ais_import_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AisImportMarkResponse]:
    packed = await AisImportMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=AisImportMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ais_import_mark(
    body: AisImportMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AisImportMarkResponse:
    saved = await AisImportMarkService(session).persist_ais_import_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        import_kind=body.import_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
