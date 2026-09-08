from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.resource import Resource
from app.services.resources.resource_service import ResourceService

router = APIRouter(prefix="/resources", tags=["resources"])

_SHIP = "can_manage_shipments"


class ResourceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resource_kind: str
    display_name: str
    registration_no: str | None = None
    source_ref: str


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    resource_kind: str
    display_name: str
    registration_no: str | None
    source_ref: str
    superseded_by: UUID | None


def _as_response(row: Resource) -> ResourceResponse:
    return ResourceResponse.model_validate(row)


@router.get("", response_model=list[ResourceResponse])
async def list_resources(
    resource_kind: str | None = Query(default=None),
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ResourceResponse]:
    kind = None if resource_kind is None or resource_kind.strip() == "" else resource_kind
    rows = await ResourceService(session).list_resources(resource_kind=kind)
    return [_as_response(row) for row in rows]


@router.post("", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    body: ResourceCreate,
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ResourceResponse:
    row = await ResourceService(session).record_resource(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        resource_kind=body.resource_kind,
        display_name=body.display_name,
        registration_no=body.registration_no,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(row)
