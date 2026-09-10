from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.circle_sim import CircleSim
from app.services.circle_sims.circle_sim_service import CircleSimService

router = APIRouter(prefix="/circle-sims", tags=["circle-sims"])

_PERM = "can_manage_circle_sims"


class CircleSimCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sim_code: str
    unload_unlocode: str
    load_unlocode: str
    source_ref: str


class CircleSimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    sim_code: str
    unload_unlocode: str
    load_unlocode: str
    source_ref: str


def _as_row(row: CircleSim) -> CircleSimResponse:
    return CircleSimResponse.model_validate(row)


@router.get("", response_model=list[CircleSimResponse])
async def list_circle_sims(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CircleSimResponse]:
    rows = await CircleSimService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=CircleSimResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_circle_sim(
    body: CircleSimCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CircleSimResponse:
    row = await CircleSimService(session).persist_circle_sim(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        sim_code=body.sim_code,
        unload_unlocode=body.unload_unlocode,
        load_unlocode=body.load_unlocode,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
