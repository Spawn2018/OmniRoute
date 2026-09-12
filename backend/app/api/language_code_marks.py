"""HTTP katalog kodu języka — HITL, bez kolumny shipment i preferred_language party."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.language_code_mark import LanguageCodeMark
from app.services.language_code_marks.language_code_mark_service import (
    LanguageCodeMarkService,
)

router = APIRouter(prefix="/language-code-marks", tags=["language-code-mark"])
_PERM = "can_manage_language_code_marks"


class LanguageCodeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    locale_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class LanguageCodeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    locale_kind: str
    source_ref: str


def _to_dto(row: LanguageCodeMark) -> LanguageCodeMarkResponse:
    return LanguageCodeMarkResponse.model_validate(row)


@router.get("", response_model=list[LanguageCodeMarkResponse])
async def list_language_code_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LanguageCodeMarkResponse]:
    catalog = LanguageCodeMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=LanguageCodeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_language_code_mark(
    body: LanguageCodeMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LanguageCodeMarkResponse:
    catalog = LanguageCodeMarkService(session)
    saved = await catalog.persist_language_code_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        locale_kind=body.locale_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "language-code-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
