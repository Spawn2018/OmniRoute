from datetime import time
from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.groupage_line import (
    require_cutoff_local,
    require_distinct_line_ends,
    require_line_code,
    require_line_location_id,
    require_line_source_ref,
    require_line_transit_days,
    require_operating_dows,
)
from app.models.groupage_line import GroupageLine
from app.repositories.groupage_lines.groupage_line_repository import GroupageLineRepository


class _LineDraft(NamedTuple):
    code: str
    origin: UUID
    dest: UUID
    cutoff: time
    days: int
    dows: list[int]
    origin_ref: str


def _line_draft(
    line_code: object,
    origin_location_id: object,
    destination_location_id: object,
    cutoff_local: object,
    transit_days: object,
    operating_dows: object,
    source_ref: object,
) -> _LineDraft:
    origin = require_line_location_id(origin_location_id, field="origin_location_id")
    dest = require_line_location_id(destination_location_id, field="destination_location_id")
    require_distinct_line_ends(origin, dest)
    return _LineDraft(
        require_line_code(line_code),
        origin,
        dest,
        require_cutoff_local(cutoff_local),
        require_line_transit_days(transit_days),
        require_operating_dows(operating_dows),
        require_line_source_ref(source_ref),
    )


def _cutoff_matches(stored: time, draft: time) -> bool:
    return time(stored.hour, stored.minute, stored.second) == draft


def _line_unchanged(current: GroupageLine, draft: _LineDraft) -> bool:
    return (
        current.origin_location_id == draft.origin
        and current.destination_location_id == draft.dest
        and _cutoff_matches(current.cutoff_local, draft.cutoff)
        and current.transit_days == draft.days
        and list(current.operating_dows) == draft.dows
        and current.source_ref == draft.origin_ref
    )


def _new_row(organization_id: UUID, user_id: UUID, draft: _LineDraft) -> GroupageLine:
    return GroupageLine(
        id=uuid4(),
        organization_id=organization_id,
        line_code=draft.code,
        origin_location_id=draft.origin,
        destination_location_id=draft.dest,
        cutoff_local=draft.cutoff,
        transit_days=draft.days,
        operating_dows=draft.dows,
        source_ref=draft.origin_ref,
        created_by=user_id,
    )


class GroupageLineService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = GroupageLineRepository(session)

    async def list_lines(self) -> list[GroupageLine]:
        return await self._rows.list_current()

    async def record_line(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        line_code: object,
        origin_location_id: object,
        destination_location_id: object,
        cutoff_local: object,
        transit_days: object,
        operating_dows: object,
        source_ref: object,
    ) -> GroupageLine:
        draft = _line_draft(
            line_code,
            origin_location_id,
            destination_location_id,
            cutoff_local,
            transit_days,
            operating_dows,
            source_ref,
        )
        current = await self._rows.find_current_by_code(draft.code)
        if current is not None and _line_unchanged(current, draft):
            return current
        saved = await self._rows.add_line(_new_row(organization_id, user_id, draft))
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
