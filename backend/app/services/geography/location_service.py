from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import (
    LocationConflict,
    NotAPostalZone,
    PostalRangeOverlap,
    ResourceNotFound,
    UnknownPostalZone,
)
from app.domain.location import (
    LocationKind,
    normalize_location_name,
    normalize_postal_bounds,
    normalize_postal_code,
    normalize_zone_code,
)
from app.domain.port import normalize_country_code
from app.models.location import Location, LocationZoneMember
from app.repositories.geography.location_repository import LocationRepository

MANUAL_SOURCE_REF = "tenant:manual"

_OVERLAP_CONSTRAINT = "ex_zone_member_no_overlap"


class LocationService:
    def __init__(self, session: AsyncSession) -> None:
        self._locations = LocationRepository(session)

    async def list_locations(
        self,
        *,
        kind: str | None = None,
        search: str | None = None,
    ) -> list[Location]:
        return await self._locations.list_all(kind=kind, search=search)

    async def list_zone_members(self, zone_id: UUID) -> list[LocationZoneMember]:
        await self._require_zone(zone_id)
        return await self._locations.list_members(zone_id)

    async def resolve_postal(self, *, country_code: str, postal_code: str) -> Location:
        country = normalize_country_code(country_code)
        code = normalize_postal_code(postal_code)
        zone = await self._locations.find_zone_by_postal(country_code=country, postal_code=code)
        if zone is None:
            raise UnknownPostalZone(f"kod {code} ({country}) nie trafia w żadną strefę tenanta")
        return zone

    async def create_zone(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
    ) -> Location:
        zone_code = normalize_zone_code(code)
        if await self._locations.find_by_code(zone_code) is not None:
            raise LocationConflict(f"strefa {zone_code} już istnieje w katalogu tenanta")

        row = Location(
            id=uuid4(),
            organization_id=organization_id,
            kind=LocationKind.POSTAL_ZONE.value,
            name=normalize_location_name(name),
            code=zone_code,
            source_ref=MANUAL_SOURCE_REF,
            created_by=user_id,
        )
        try:
            return await self._locations.add_location(row)
        except IntegrityError as exc:
            raise LocationConflict(
                f"strefa {zone_code} już istnieje w katalogu tenanta"
            ) from exc

    async def add_zone_member(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        zone_id: UUID,
        country_code: str,
        postal_from: str,
        postal_to: str,
    ) -> LocationZoneMember:
        await self._require_zone(zone_id)
        lower, upper = normalize_postal_bounds(postal_from, postal_to)

        row = LocationZoneMember(
            id=uuid4(),
            organization_id=organization_id,
            zone_location_id=zone_id,
            country_code=normalize_country_code(country_code),
            postal_from=lower,
            postal_to=upper,
            source_ref=MANUAL_SOURCE_REF,
            created_by=user_id,
        )
        try:
            return await self._locations.add_member(row)
        except IntegrityError as exc:
            if _OVERLAP_CONSTRAINT in str(exc.orig):
                raise PostalRangeOverlap(
                    f"zakres {lower}-{upper} nachodzi na istniejący w strefie"
                ) from exc
            raise

    async def _require_zone(self, zone_id: UUID) -> Location:
        zone = await self._locations.get(zone_id)
        if zone is None:
            raise ResourceNotFound(f"strefa {zone_id} nie istnieje w katalogu tenanta")
        if zone.kind != LocationKind.POSTAL_ZONE.value:
            raise NotAPostalZone(f"lokalizacja {zone_id} nie jest strefą pocztową")
        return zone
