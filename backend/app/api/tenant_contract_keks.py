from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tenant_contract_kek import TenantContractKek
from app.services.tenant_contract_keks.tenant_contract_kek_service import (
    TenantContractKekService,
)

router = APIRouter(prefix="/tenant-contract-keks", tags=["tenant-contract-keks"])

_PERM = "can_manage_tenant_contract_keks"


class TenantContractKekCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kek_code: str
    wrap_kind: str
    source_ref: str


class TenantContractKekResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    kek_code: str
    wrap_kind: str
    source_ref: str


def _as_mark(mark: TenantContractKek) -> TenantContractKekResponse:
    return TenantContractKekResponse(
        id=mark.id,
        organization_id=mark.organization_id,
        kek_code=mark.kek_code,
        wrap_kind=mark.wrap_kind,
        source_ref=mark.source_ref,
    )


@router.get("", response_model=list[TenantContractKekResponse])
async def list_tenant_contract_keks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenantContractKekResponse]:
    marks = await TenantContractKekService(session).list_marks()
    return [_as_mark(mark) for mark in marks]


@router.post(
    "",
    response_model=TenantContractKekResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tenant_contract_kek(
    body: TenantContractKekCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenantContractKekResponse:
    mark = await TenantContractKekService(session).persist_kek_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        kek_code=body.kek_code,
        wrap_kind=body.wrap_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_mark(mark)
