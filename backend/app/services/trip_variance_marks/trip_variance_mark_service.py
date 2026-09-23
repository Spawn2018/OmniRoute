from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import TripVarianceMarkConflict
from app.domain.trip_variance_mark import parse_trip_variance_mark_row
from app.models.trip_variance_mark import TripVarianceMark
from app.repositories.trip_variance_marks.trip_variance_mark_repository import (
    TripVarianceMarkRepository,
)


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_trip_variance_mark_org_code" in detail:
        raise TripVarianceMarkConflict(
            "ten kod wariancji przejazdu już istnieje",
        ) from orig
    if "uq_trip_variance_mark_org_source_ref" in detail:
        raise TripVarianceMarkConflict(
            "to wskazanie wariancji przejazdu już istnieje",
        ) from orig
    raise orig


class TripVarianceMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = TripVarianceMarkRepository(session)

    async def list_marks(self) -> list[TripVarianceMark]:
        return await self._repo.list_marks()

    async def persist_trip_variance_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        variance_kind: object,
        source_ref: object,
    ) -> TripVarianceMark:
        code, kind, origin = parse_trip_variance_mark_row(
            mark_code,
            variance_kind,
            source_ref,
        )
        row = TripVarianceMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            variance_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._repo.add_mark(row)
        except IntegrityError as exc:
            _raise_create_conflict(exc)
