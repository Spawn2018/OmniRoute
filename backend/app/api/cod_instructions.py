from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cod_instruction import CodInstruction
from app.services.cod_instructions.cod_instruction_service import CodInstructionService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/cod-instructions", tags=["cod-instructions"])

_PERM = "can_manage_cod_instructions"


class CodInstructionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    instruction_code: str
    collection_status: str
    source_ref: str


class CodInstructionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    instruction_code: str
    collection_status: str
    source_ref: str


def _as_row(row: CodInstruction) -> CodInstructionResponse:
    return CodInstructionResponse.model_validate(row)


@router.get("", response_model=list[CodInstructionResponse])
async def list_cod_instructions(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CodInstructionResponse]:
    rows = await CodInstructionService(session).list_instructions()
    return [_as_row(row) for row in rows]


@router.post("", response_model=CodInstructionResponse, status_code=status.HTTP_201_CREATED)
async def create_cod_instruction(
    body: CodInstructionCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CodInstructionResponse:
    order = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await CodInstructionService(session).record_instruction(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=order.id,
        instruction_code=body.instruction_code,
        collection_status=body.collection_status,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
