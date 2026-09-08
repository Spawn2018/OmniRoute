from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.resource import (
    require_display_name,
    require_registration_no,
    require_resource_kind,
    require_resource_source_ref,
)
from app.models.resource import Resource
from app.repositories.resources.resource_repository import ResourceRepository


class _FleetDraft(NamedTuple):
    kind: str
    label: str
    plate: str | None
    origin: str


def _fleet_draft(
    resource_kind: object,
    display_name: object,
    registration_no: object,
    source_ref: object,
) -> _FleetDraft:
    return _FleetDraft(
        require_resource_kind(resource_kind),
        require_display_name(display_name),
        require_registration_no(registration_no),
        require_resource_source_ref(source_ref),
    )


def _plate_unchanged(current: Resource, draft: _FleetDraft) -> bool:
    return current.registration_no == draft.plate and current.source_ref == draft.origin


class ResourceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ResourceRepository(session)

    async def list_resources(self, *, resource_kind: object | None = None) -> list[Resource]:
        kind = None if resource_kind is None else require_resource_kind(resource_kind)
        return await self._rows.list_current(kind)

    async def record_resource(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        resource_kind: object,
        display_name: object,
        registration_no: object,
        source_ref: object,
    ) -> Resource:
        draft = _fleet_draft(resource_kind, display_name, registration_no, source_ref)
        current = await self._rows.find_current(draft.kind, draft.label)
        if current is not None and _plate_unchanged(current, draft):
            return current
        saved = await self._rows.add(
            Resource(
                id=uuid4(),
                organization_id=organization_id,
                resource_kind=draft.kind,
                display_name=draft.label,
                registration_no=draft.plate,
                source_ref=draft.origin,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
