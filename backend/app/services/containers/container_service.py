from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.container import (
    require_container_no,
    require_container_shipment_id,
    require_container_source_ref,
    require_iso_size_type,
    require_seal_no_1,
)
from app.models.container import Container
from app.repositories.containers.container_repository import ContainerRepository


class _BoxDraft(NamedTuple):
    number: str
    size_type: str
    shipment_id: UUID | None
    origin: str
    seal: str | None


def _box_draft(
    container_no: object,
    iso_size_type: object,
    shipment_id: object,
    source_ref: object,
    seal_no_1: object,
) -> _BoxDraft:
    return _BoxDraft(
        require_container_no(container_no),
        require_iso_size_type(iso_size_type),
        require_container_shipment_id(shipment_id),
        require_container_source_ref(source_ref),
        require_seal_no_1(seal_no_1),
    )


def _box_unchanged(current: Container, draft: _BoxDraft) -> bool:
    return (
        current.iso_size_type == draft.size_type
        and current.shipment_id == draft.shipment_id
        and current.source_ref == draft.origin
        and current.seal_no_1 == draft.seal
    )


class ContainerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ContainerRepository(session)

    async def list_containers(self, *, iso_size_type: object | None = None) -> list[Container]:
        size_type = None if iso_size_type is None else require_iso_size_type(iso_size_type)
        return await self._rows.list_current(size_type)

    async def record_container(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        container_no: object,
        iso_size_type: object,
        shipment_id: object,
        source_ref: object,
        seal_no_1: object = None,
    ) -> Container:
        draft = _box_draft(container_no, iso_size_type, shipment_id, source_ref, seal_no_1)
        current = await self._rows.find_current(draft.number)
        if current is not None and _box_unchanged(current, draft):
            return current
        saved = await self._rows.add(
            Container(
                id=uuid4(),
                organization_id=organization_id,
                container_no=draft.number,
                iso_size_type=draft.size_type,
                shipment_id=draft.shipment_id,
                source_ref=draft.origin,
                seal_no_1=draft.seal,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
