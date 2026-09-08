from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidNetworkCode, NetworkConflict, UnknownNetwork
from app.domain.network import (
    normalize_network_aliases,
    normalize_network_code,
    optional_network_text,
    require_network_member_name,
)
from app.models.network import Network
from app.models.network_member import NetworkMember
from app.repositories.networks.network_member_repository import NetworkMemberRepository
from app.repositories.networks.network_repository import NetworkRepository

_MANUAL = "tenant:manual"


class NetworkService:
    def __init__(self, session: AsyncSession) -> None:
        self._networks = NetworkRepository(session)
        self._members = NetworkMemberRepository(session)

    async def list_networks(self) -> list[Network]:
        return await self._networks.list_all()

    async def create_network(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
        aliases: list[str],
        website: str | None,
        region_scope: str | None,
        is_global: bool,
    ) -> Network:
        token = normalize_network_code(code)
        alias_tokens = normalize_network_aliases(aliases)
        if token in alias_tokens:
            raise InvalidNetworkCode("alias nie może powielać kodu")
        label = name.strip()
        if label == "":
            raise InvalidNetworkCode("nazwa sieci jest wymagana")
        await self._reject_taken([token, *alias_tokens])
        row = Network(
            id=uuid4(),
            organization_id=organization_id,
            code=token,
            name=label,
            aliases=alias_tokens,
            website=optional_network_text(website, limit=256, field="strona"),
            region_scope=optional_network_text(region_scope, limit=64, field="zakres"),
            is_global=is_global,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._networks.add(row)
        except IntegrityError as exc:
            raise NetworkConflict(f"sieć {token} już istnieje") from exc

    async def resolve(self, raw: str) -> Network:
        token = normalize_network_code(raw)
        found = await self._networks.find_by_token(token)
        if found is None:
            raise UnknownNetwork(f"nieznana sieć: {token}")
        return found

    async def get_network(self, network_id: UUID) -> Network:
        found = await self._networks.get(network_id)
        if found is None:
            raise UnknownNetwork(f"nieznana sieć: {network_id}")
        return found

    async def list_members(self, network_id: UUID) -> list[NetworkMember]:
        await self.get_network(network_id)
        return await self._members.list_for_network(network_id)

    async def create_member(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        network_id: UUID,
        member_code: str,
        legal_name: str,
        party_id: UUID,
    ) -> NetworkMember:
        network = await self.get_network(network_id)
        token = normalize_network_code(member_code)
        row = NetworkMember(
            id=uuid4(),
            organization_id=organization_id,
            network_id=network.id,
            member_code=token,
            legal_name=require_network_member_name(legal_name),
            party_id=party_id,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._members.add(row)
        except IntegrityError as exc:
            raise NetworkConflict(f"członek {token} już istnieje w sieci") from exc

    async def _reject_taken(self, tokens: list[str]) -> None:
        for token in tokens:
            existing = await self._networks.find_by_token(token)
            if existing is not None:
                raise NetworkConflict(f"sieć {token} już istnieje")
