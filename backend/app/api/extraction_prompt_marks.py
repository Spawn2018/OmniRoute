from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.extraction_prompt_mark import ExtractionPromptMark
from app.services.extraction_prompt_marks.extraction_prompt_mark_service import (
    ExtractionPromptMarkService,
)

router = APIRouter(prefix="/extraction-prompt-marks", tags=["extraction-prompt-marks"])


class ExtractionPromptMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(description="snake HITL")
    prompt_kind: str = Field(description="extract|system|other")
    source_ref: str = Field(description="tenant:manual lub fixture")


class ExtractionPromptMarkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    prompt_kind: str
    source_ref: str


@router.get("", response_model=list[ExtractionPromptMarkOut])
async def list_extraction_prompt_marks(
    _authz: None = Depends(
        require_permission("can_manage_extraction_prompt_marks", "organization"),
    ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ExtractionPromptMarkOut]:
    service = ExtractionPromptMarkService(session)
    return [ExtractionPromptMarkOut.model_validate(row) for row in await service.list_marks()]


@router.post("", response_model=ExtractionPromptMarkOut, status_code=status.HTTP_201_CREATED)
async def create_extraction_prompt_mark(
    body: ExtractionPromptMarkCreate,
    _authz: None = Depends(
        require_permission("can_manage_extraction_prompt_marks", "organization"),
    ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ExtractionPromptMarkOut:
    service = ExtractionPromptMarkService(session)
    saved: ExtractionPromptMark = await service.persist_extraction_prompt_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        prompt_kind=body.prompt_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return ExtractionPromptMarkOut.model_validate(saved)
