from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.customer_contract import CustomerContract
from app.services.customer_contracts.customer_contract_service import CustomerContractService

router = APIRouter(prefix="/customer-contracts", tags=["customer-contracts"])

_PERM = "can_manage_customer_contracts"


class CustomerContractCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_code: str
    shipper_label: str
    their_customer_label: str
    source_ref: str
    opaque_fixture: bool = False
    opaque_blob: str | None = None


class CustomerContractResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    contract_code: str
    shipper_label: str
    their_customer_label: str
    source_ref: str
    has_ciphertext: bool


def _as_row(row: CustomerContract) -> CustomerContractResponse:
    return CustomerContractResponse(
        id=row.id,
        organization_id=row.organization_id,
        contract_code=row.contract_code,
        shipper_label=row.shipper_label,
        their_customer_label=row.their_customer_label,
        source_ref=row.source_ref,
        has_ciphertext=row.has_ciphertext,
    )


@router.get("", response_model=list[CustomerContractResponse])
async def list_customer_contracts(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CustomerContractResponse]:
    rows = await CustomerContractService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=CustomerContractResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_contract(
    payload: CustomerContractCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CustomerContractResponse:
    row = await CustomerContractService(session).persist_customer_contract(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        contract_code=payload.contract_code,
        shipper_label=payload.shipper_label,
        their_customer_label=payload.their_customer_label,
        source_ref=payload.source_ref,
        opaque_fixture=payload.opaque_fixture,
        opaque_blob=payload.opaque_blob,
    )
    await session.commit()
    return _as_row(row)
