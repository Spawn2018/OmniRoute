from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidPortData, PortConflict, ResourceNotFound
from app.domain.port import (
    normalize_country_code,
    normalize_port_aliases,
    normalize_port_token,
    normalize_unlocode,
    select_resolved_port,
)
from app.models.port import Port
from app.repositories.geography.port_repository import PortRepository

MANUAL_SOURCE_REF = "tenant:manual"


class PortService:
    def __init__(self, session: AsyncSession) -> None:
        self._ports = PortRepository(session)

    async def list_ports(self, search: str | None = None) -> list[Port]:
        return await self._ports.list_all(search)

    async def get_port(self, port_id: UUID) -> Port:
        found = await self._ports.get(port_id)
        if found is None:
            raise ResourceNotFound("nieznany port")
        return found

    async def resolve(self, raw: str) -> Port:
        token = normalize_port_token(raw)
        candidates = await self._ports.find_by_token(
            unlocode=token.replace(" ", ""),
            alias=token,
        )
        return select_resolved_port(token, candidates)

    async def create_manual_port(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        unlocode: str,
        name: str,
        country_code: str,
        lat: Decimal | None,
        lng: Decimal | None,
        is_seaport: bool,
        function_flags: list[str],
        aliases: list[str],
    ) -> Port:
        code = normalize_unlocode(unlocode)
        label = name.strip()
        if label == "":
            raise InvalidPortData("nazwa portu jest wymagana")
        if await self._ports.find_by_unlocode(code) is not None:
            raise PortConflict(f"port {code} już istnieje w katalogu tenanta")

        row = Port(
            id=uuid4(),
            organization_id=organization_id,
            unlocode=code,
            name=label,
            country_code=normalize_country_code(country_code),
            lat=lat,
            lng=lng,
            is_seaport=is_seaport,
            function_flags=list(function_flags),
            aliases=normalize_port_aliases(aliases),
            is_official=False,
            source_ref=MANUAL_SOURCE_REF,
            created_by=user_id,
        )
        try:
            return await self._ports.add(row)
        except IntegrityError as exc:
            raise PortConflict(f"port {code} już istnieje w katalogu tenanta") from exc
