from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import TerminalConflict, UnknownTerminal
from app.domain.terminal import (
    normalize_isps_code,
    normalize_operator_name,
    normalize_terminal_name,
)
from app.models.terminal import Terminal
from app.repositories.geography.terminal_repository import TerminalRepository

MANUAL_SOURCE_REF = "tenant:manual"


class TerminalService:
    def __init__(self, session: AsyncSession) -> None:
        self._terminals = TerminalRepository(session)

    async def list_terminals(
        self,
        *,
        port_id: UUID | None = None,
        search: str | None = None,
    ) -> list[Terminal]:
        return await self._terminals.list_all(port_id=port_id, search=search)

    async def resolve(self, raw: str) -> Terminal:
        token = normalize_isps_code(raw)
        if token is None:
            raise UnknownTerminal("nieznany terminal: ")
        found = await self._terminals.find_by_isps(token)
        if found is None:
            raise UnknownTerminal(f"nieznany terminal: {token}")
        return found

    async def create_terminal(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        port_id: UUID,
        name: str,
        isps_code: str | None,
        operator_name: str | None,
        lat: Decimal | None,
        lng: Decimal | None,
        operator_party_id: UUID | None = None,
    ) -> Terminal:
        row = Terminal(
            id=uuid4(),
            organization_id=organization_id,
            port_id=port_id,
            name=normalize_terminal_name(name),
            isps_code=normalize_isps_code(isps_code),
            operator_name=normalize_operator_name(operator_name),
            operator_party_id=operator_party_id,
            lat=lat,
            lng=lng,
            source_ref=MANUAL_SOURCE_REF,
            created_by=user_id,
        )
        try:
            return await self._terminals.add(row)
        except IntegrityError as exc:
            raise TerminalConflict(
                "terminal o tym kodzie ISPS albo nazwie przy porcie już istnieje"
            ) from exc
