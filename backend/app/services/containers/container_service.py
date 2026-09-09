from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.container import (
    require_cargo_description,
    require_container_no,
    require_container_ref_1,
    require_container_ref_2,
    require_container_ref_3,
    require_container_ref_4,
    require_container_ref_5,
    require_container_remarks,
    require_container_shipment_id,
    require_container_source_ref,
    require_iso_size_type,
    require_packaging_code,
    require_seal_no_1,
    require_seal_no_2,
    require_seal_no_3,
    require_vessel_name,
    require_voyage_no,
)
from app.models.container import Container
from app.repositories.containers.container_repository import ContainerRepository


class _WriteBox(NamedTuple):
    number: object
    size_type: object
    shipment_id: object
    origin: object
    seal: object
    seal2: object
    seal3: object
    vessel: object
    voyage: object
    note: object
    goods: object
    pack: object
    mark: object
    mark2: object
    mark3: object
    mark4: object
    mark5: object


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
    pack: str | None
    mark: str | None
    mark2: str | None
    mark3: str | None
    mark4: str | None
    mark5: str | None


def _box_draft(write: _WriteBox) -> _BoxDraft:
    return _BoxDraft(
        require_container_no(write.number),
        require_iso_size_type(write.size_type),
        require_container_shipment_id(write.shipment_id),
        require_container_source_ref(write.origin),
        require_seal_no_1(write.seal),
        require_seal_no_2(write.seal2),
        require_seal_no_3(write.seal3),
        require_vessel_name(write.vessel),
        require_voyage_no(write.voyage),
        require_container_remarks(write.note),
        require_cargo_description(write.goods),
        require_packaging_code(write.pack),
        require_container_ref_1(write.mark),
        require_container_ref_2(write.mark2),
        require_container_ref_3(write.mark3),
        require_container_ref_4(write.mark4),
        require_container_ref_5(write.mark5),
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
        and current.packaging_code == draft.pack
        and current.ref_1 == draft.mark
        and current.ref_2 == draft.mark2
        and current.ref_3 == draft.mark3
        and current.ref_4 == draft.mark4
        and current.ref_5 == draft.mark5
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
        packaging_code=draft.pack,
        ref_1=draft.mark,
        ref_2=draft.mark2,
        ref_3=draft.mark3,
        ref_4=draft.mark4,
        ref_5=draft.mark5,
        created_by=user_id,
    )


class ContainerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ContainerRepository(session)

    async def list_containers(self, *, iso_size_type: object | None = None) -> list[Container]:
        size_type = None if iso_size_type is None else require_iso_size_type(iso_size_type)
        return await self._rows.list_current(size_type)

    async def _persist_box(
        self,
        organization_id: UUID,
        user_id: UUID,
        draft: _BoxDraft,
    ) -> Container:
        current = await self._rows.find_current(draft.number)
        if current is not None and _box_unchanged(current, draft):
            return current
        saved = await self._rows.add(_container_row(organization_id, user_id, draft))
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved

    async def record_container(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        write: _WriteBox,
    ) -> Container:
        return await self._persist_box(organization_id, user_id, _box_draft(write))
