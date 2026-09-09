from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.carbon_method import CarbonMethod
from app.services.carbon_methods.carbon_method_service import CarbonMethodService

router = APIRouter(prefix="/carbon-methods", tags=["carbon-methods"])

_PERM = "can_manage_carbon_methods"


class CarbonMethodCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method_code: str
    method_version: str
    source_ref: str


class CarbonMethodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    method_code: str
    method_version: str
    source_ref: str


def _as_row(row: CarbonMethod) -> CarbonMethodResponse:
    return CarbonMethodResponse(
        id=row.id,
        organization_id=row.organization_id,
        method_code=row.method_code,
        method_version=row.method_version,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[CarbonMethodResponse])
async def list_carbon_methods(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CarbonMethodResponse]:
    rows = await CarbonMethodService(session).list_methods()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=CarbonMethodResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_carbon_method(
    body: CarbonMethodCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CarbonMethodResponse:
    row = await CarbonMethodService(session).persist_method(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        method_code=body.method_code,
        method_version=body.method_version,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
