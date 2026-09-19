from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.resource import (
    require_capacity_kg,
    require_capacity_ldm,
    require_capacity_m3,
    require_display_name,
    require_inventory_no,
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
    inventory: str | None
    capacity: object
    ldm: object
    cubic: object
    origin: str


def _fleet_draft(
    resource_kind: object,
    display_name: object,
    registration_no: object,
    inventory_no: object,
    capacity_kg: object,
    capacity_ldm: object,
    capacity_m3: object,
    source_ref: object,
) -> _FleetDraft:
    return _FleetDraft(
        require_resource_kind(resource_kind),
        require_display_name(display_name),
        require_registration_no(registration_no),
        require_inventory_no(inventory_no),
        require_capacity_kg(capacity_kg),
        require_capacity_ldm(capacity_ldm),
        require_capacity_m3(capacity_m3),
        require_resource_source_ref(source_ref),
    )


def _fleet_unchanged(current: Resource, draft: _FleetDraft) -> bool:
    return (
        current.registration_no == draft.plate
        and current.inventory_no == draft.inventory
        and current.capacity_kg == draft.capacity
        and current.capacity_ldm == draft.ldm
        and current.capacity_m3 == draft.cubic
        and current.source_ref == draft.origin
    )


class ResourceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ResourceRepository(session)

    async def list_resources(self, *, resource_kind: object | None = None) -> list[Resource]:
        kind = None if resource_kind is None else require_resource_kind(resource_kind)
        return await self._rows.list_current(kind)

    async def get_resource(self, resource_id: UUID) -> Resource:
        found = await self._rows.get(resource_id)
        if found is None:
            raise ResourceNotFound("nieznany zasób")
        return found

    async def record_resource(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        resource_kind: object,
        display_name: object,
        registration_no: object,
        inventory_no: object = None,
        capacity_kg: object = None,
        capacity_ldm: object = None,
        capacity_m3: object = None,
        source_ref: object,
    ) -> Resource:
        draft = _fleet_draft(
            resource_kind,
            display_name,
            registration_no,
            inventory_no,
            capacity_kg,
            capacity_ldm,
            capacity_m3,
            source_ref,
        )
        current = await self._rows.find_current(draft.kind, draft.label)
        if current is not None and _fleet_unchanged(current, draft):
            return current
        saved = await self._rows.add(_new_resource(organization_id, user_id, draft))
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved


def _new_resource(organization_id: UUID, user_id: UUID, draft: _FleetDraft) -> Resource:
    return Resource(
        id=uuid4(),
        organization_id=organization_id,
        resource_kind=draft.kind,
        display_name=draft.label,
        registration_no=draft.plate,
        inventory_no=draft.inventory,
        capacity_kg=draft.capacity,
        capacity_ldm=draft.ldm,
        capacity_m3=draft.cubic,
        source_ref=draft.origin,
        created_by=user_id,
    )