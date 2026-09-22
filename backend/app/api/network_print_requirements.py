from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.network_print_requirement import NetworkPrintRequirement
from app.services.network_print_requirements.network_print_requirement_service import (
    NetworkPrintRequirementService,
)

router = APIRouter(
    prefix="/network-print-requirements",
    tags=["network-print-requirements"],
)

_PERM = "can_manage_network_print_requirements"


class NetworkPrintRequirementCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirement_code: str
    network_label: str
    source_ref: str


class NetworkPrintRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    requirement_code: str
    network_label: str
    source_ref: str


def _row(saved: NetworkPrintRequirement) -> NetworkPrintRequirementResponse:
    return NetworkPrintRequirementResponse.model_validate(saved)


@router.get("", response_model=list[NetworkPrintRequirementResponse])
async def list_network_print_requirements(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NetworkPrintRequirementResponse]:
    packed = await NetworkPrintRequirementService(session).list_requirements()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=NetworkPrintRequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_network_print_requirement(
    body: NetworkPrintRequirementCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NetworkPrintRequirementResponse:
    saved = await NetworkPrintRequirementService(
        session,
    ).persist_network_print_requirement(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        requirement_code=body.requirement_code,
        network_label=body.network_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
