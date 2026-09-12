"""HTTP katalog spot/contract — HITL, bez FK quotation i cargo_value."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.spot_contract_mark import SpotContractMark
from app.services.spot_contract_marks.spot_contract_mark_service import (
    SpotContractMarkService,
)

router = APIRouter(prefix="/spot-contract-marks", tags=["spot-contract-mark"])
_PERM = "can_manage_spot_contract_marks"


class SpotContractMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    deal_kind: str = Field(min_length=4, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class SpotContractMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    deal_kind: str
    source_ref: str


def _to_dto(row: SpotContractMark) -> SpotContractMarkResponse:
    return SpotContractMarkResponse.model_validate(row)


@router.get("", response_model=list[SpotContractMarkResponse])
async def list_spot_contract_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SpotContractMarkResponse]:
    catalog = SpotContractMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=SpotContractMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_spot_contract_mark(
    body: SpotContractMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SpotContractMarkResponse:
    catalog = SpotContractMarkService(session)
    saved = await catalog.persist_spot_contract_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        deal_kind=body.deal_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "spot-contract-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
