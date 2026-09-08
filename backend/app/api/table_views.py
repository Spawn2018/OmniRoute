from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.tenancy.table_view_service import TableViewService

router = APIRouter(prefix="/tenancy/table-views", tags=["table-views"])


class TableViewConfig(BaseModel):
    column_order: list[str] = Field(default_factory=list)
    column_visibility: dict[str, bool] = Field(default_factory=dict)
    filters: dict[str, Any] = Field(default_factory=dict)
    sorting: list[dict[str, str]] = Field(default_factory=list)
    density: str = "compact"
    group_by: str | None = None


class TableViewCreate(BaseModel):
    table_key: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=128)
    config: TableViewConfig = Field(default_factory=TableViewConfig)


class TableViewUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    config: TableViewConfig | None = None


class TableViewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    user_id: UUID
    table_key: str
    name: str
    config: dict[str, Any]


@router.get("", response_model=list[TableViewResponse])
async def list_table_views(
    table_key: str = Query(..., min_length=1, max_length=128),
    _authz: None = Depends(require_permission("can_manage_table_views", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> list[TableViewResponse]:
    service = TableViewService(session)
    views = await service.list_views(identity.user_id, table_key)
    return [TableViewResponse.model_validate(view) for view in views]


@router.post("", response_model=TableViewResponse, status_code=status.HTTP_201_CREATED)
async def create_table_view(
    body: TableViewCreate,
    _authz: None = Depends(require_permission("can_manage_table_views", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TableViewResponse:
    service = TableViewService(session)
    view = await service.create_view(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        table_key=body.table_key,
        name=body.name,
        config=body.config.model_dump(),
    )
    await session.commit()
    return TableViewResponse.model_validate(view)


@router.patch("/{view_id}", response_model=TableViewResponse)
async def update_table_view(
    view_id: UUID,
    body: TableViewUpdate,
    _authz: None = Depends(require_permission("can_manage_table_views", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TableViewResponse:
    service = TableViewService(session)
    view = await service.update_view(
        view_id=view_id,
        user_id=identity.user_id,
        name=body.name,
        config=body.config.model_dump() if body.config is not None else None,
    )
    await session.commit()
    return TableViewResponse.model_validate(view)


@router.delete("/{view_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table_view(
    view_id: UUID,
    _authz: None = Depends(require_permission("can_manage_table_views", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> Response:
    service = TableViewService(session)
    await service.delete_view(view_id, identity.user_id)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
