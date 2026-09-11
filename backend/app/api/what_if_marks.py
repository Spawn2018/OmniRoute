from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.what_if_mark import WhatIfMark
from app.services.what_if_marks.what_if_mark_service import (
    WhatIfMarkService,
)

router = APIRouter(prefix="/what-if-marks", tags=["what-if-marks"])

_PERM = "can_manage_what_if_marks"


class WhatIfMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    scenario_kind: str
    source_ref: str


class WhatIfMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    scenario_kind: str
    source_ref: str


def _row(saved: WhatIfMark) -> WhatIfMarkResponse:
    return WhatIfMarkResponse.model_validate(saved)


@router.get("", response_model=list[WhatIfMarkResponse])
async def list_what_if_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[WhatIfMarkResponse]:
    packed = await WhatIfMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=WhatIfMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_what_if_mark(
    body: WhatIfMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> WhatIfMarkResponse:
    saved = await WhatIfMarkService(session).persist_what_if_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        scenario_kind=body.scenario_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
