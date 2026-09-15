from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.data_source import DataSource
from app.services.data_sources.data_source_service import DataSourceService

router = APIRouter(
    prefix="/data-sources",
    tags=["data-sources"],
)

_PERM = "can_manage_data_sources"


class DataSourceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_code: str
    license_label: str
    rights_scope: str
    source_ref: str


class DataSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    source_code: str
    license_label: str
    rights_scope: str
    source_ref: str


def _row(saved: DataSource) -> DataSourceResponse:
    return DataSourceResponse.model_validate(saved)


@router.get("", response_model=list[DataSourceResponse])
async def list_data_sources(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DataSourceResponse]:
    packed = await DataSourceService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=DataSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_data_source(
    body: DataSourceCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DataSourceResponse:
    saved = await DataSourceService(session).persist_data_source(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        source_code=body.source_code,
        license_label=body.license_label,
        rights_scope=body.rights_scope,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
