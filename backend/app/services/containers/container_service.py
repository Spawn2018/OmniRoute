from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.container import (
    require_cargo_description,
    require_container_no,
    require_container_remarks,
    require_container_shipment_id,
    require_container_source_ref,
    require_iso_size_type,
    require_seal_no_1,
    require_seal_no_2,
    require_seal_no_3,
    require_vessel_name,
    require_voyage_no,
)
from app.models.container import Container
from app.repositories.containers.container_repository import ContainerRepository


class _BoxDraft(NamedTuple):
    number: str
    size_type: str
    shipment_id: UUID | None
    origin: str
    seal: str | None
    seal2: str | None
    seal3: str | None
    vessel: str | None
    voyage: str | None
    note: str | None
    goods: str | None


def _box_draft(
    container_no: object,
    iso_size_type: object,
    shipment_id: object,
    source_ref: object,
    seal_no_1: object,
    seal_no_2: object,
    seal_no_3: object,
    vessel_name: object,
    voyage_no: object,
    remarks: object,
    cargo_description: object,
) -> _BoxDraft:
    return _BoxDraft(
        require_container_no(container_no),
        require_iso_size_type(iso_size_type),
        require_container_shipment_id(shipment_id),
        require_container_source_ref(source_ref),
        require_seal_no_1(seal_no_1),
        require_seal_no_2(seal_no_2),
        require_seal_no_3(seal_no_3),
        require_vessel_name(vessel_name),
        require_voyage_no(voyage_no),
        require_container_remarks(remarks),
        require_cargo_description(cargo_description),
    )


def _box_unchanged(current: Container, draft: _BoxDraft) -> bool:
    return (
        current.iso_size_type == draft.size_type
        and current.shipment_id == draft.shipment_id
        and current.source_ref == draft.origin
        and current.seal_no_1 == draft.seal
        and current.seal_no_2 == draft.seal2
        and current.seal_no_3 == draft.seal3
        and current.vessel_name == draft.vessel
        and current.voyage_no == draft.voyage
        and current.remarks == draft.note
        and current.cargo_description == draft.goods
    )


def _container_row(organization_id: UUID, user_id: UUID, draft: _BoxDraft) -> Container:
    return Container(
        id=uuid4(),
        organization_id=organization_id,
        container_no=draft.number,
        iso_size_type=draft.size_type,
        shipment_id=draft.shipment_id,
        source_ref=draft.origin,
        seal_no_1=draft.seal,
        seal_no_2=draft.seal2,
        seal_no_3=draft.seal3,
        vessel_name=draft.vessel,
        voyage_no=draft.voyage,
        remarks=draft.note,
        cargo_description=draft.goods,
        created_by=user_id,
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
        seal_no_2: object = None,
        seal_no_3: object = None,
        vessel_name: object = None,
        voyage_no: object = None,
        remarks: object = None,
        cargo_description: object = None,
    ) -> Container:
        draft = _box_draft(
            container_no,
            iso_size_type,
            shipment_id,
            source_ref,
            seal_no_1,
            seal_no_2,
            seal_no_3,
            vessel_name,
            voyage_no,
            remarks,
            cargo_description,
        )
        current = await self._rows.find_current(draft.number)
        if current is not None and _box_unchanged(current, draft):
            return current
        saved = await self._rows.add(_container_row(organization_id, user_id, draft))
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
