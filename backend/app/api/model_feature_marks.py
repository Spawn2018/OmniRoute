from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.model_feature_mark import ModelFeatureMark
from app.services.model_feature_marks.model_feature_mark_service import (
    ModelFeatureMarkService,
)

router = APIRouter(
    prefix="/model-feature-marks",
    tags=["model-feature-marks"],
)

_PERM = "can_manage_model_feature_marks"


class ModelFeatureMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    feature_kind: str
    source_ref: str


class ModelFeatureMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    feature_kind: str
    source_ref: str


def _row(saved: ModelFeatureMark) -> ModelFeatureMarkResponse:
    return ModelFeatureMarkResponse.model_validate(saved)


@router.get("", response_model=list[ModelFeatureMarkResponse])
async def list_model_feature_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ModelFeatureMarkResponse]:
    packed = await ModelFeatureMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ModelFeatureMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_model_feature_mark(
    body: ModelFeatureMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ModelFeatureMarkResponse:
    saved = await ModelFeatureMarkService(session).persist_model_feature_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        feature_kind=body.feature_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
