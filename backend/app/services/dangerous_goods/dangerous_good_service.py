from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dangerous_good import (
    normalize_adr_tunnel_code,
    normalize_imdg_class,
    normalize_packing_group,
    normalize_segregation_group,
    normalize_un_aliases,
    normalize_un_number,
    require_limited_quantity,
    require_marine_pollutant,
)
from app.domain.errors import (
    DangerousGoodConflict,
    InvalidDangerousGood,
    UnknownDangerousGood,
)
from app.models.dangerous_good import DangerousGood
from app.repositories.dangerous_goods.dangerous_good_repository import DangerousGoodRepository

_MANUAL = "tenant:manual"


class _NormalizedGood(NamedTuple):
    un_number: str
    imdg_class: str
    adr_tunnel_code: str
    segregation_group: str
    packing_group: str
    marine_pollutant: bool
    limited_quantity: bool
    name: str
    aliases: list[str]


class DangerousGoodService:
    def __init__(self, session: AsyncSession) -> None:
        self._goods = DangerousGoodRepository(session)

    async def list_goods(self) -> list[DangerousGood]:
        return await self._goods.list_all()

    async def get(self, good_id: UUID) -> DangerousGood:
        found = await self._goods.get(good_id)
        if found is None:
            raise UnknownDangerousGood(f"nieznany towar niebezpieczny: {good_id}")
        return found

    async def create_good(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        un_number: str,
        imdg_class: str,
        name: str,
        aliases: list[str],
        adr_tunnel_code: str,
        segregation_group: str,
        packing_group: str,
        marine_pollutant: bool,
        limited_quantity: bool,
    ) -> DangerousGood:
        draft = self._normalized_create_inputs(
            un_number=un_number,
            imdg_class=imdg_class,
            name=name,
            aliases=aliases,
            adr_tunnel_code=adr_tunnel_code,
            segregation_group=segregation_group,
            packing_group=packing_group,
            marine_pollutant=marine_pollutant,
            limited_quantity=limited_quantity,
        )
        await self._reject_taken([draft.un_number, *draft.aliases])
        return await self._insert_from_draft(organization_id, user_id, draft)

    async def _insert_from_draft(
        self,
        organization_id: UUID,
        user_id: UUID,
        draft: _NormalizedGood,
    ) -> DangerousGood:
        row = DangerousGood(
            id=uuid4(),
            organization_id=organization_id,
            un_number=draft.un_number,
            imdg_class=draft.imdg_class,
            adr_tunnel_code=draft.adr_tunnel_code,
            segregation_group=draft.segregation_group,
            packing_group=draft.packing_group,
            marine_pollutant=draft.marine_pollutant,
            limited_quantity=draft.limited_quantity,
            name=draft.name,
            aliases=draft.aliases,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._goods.add(row)
        except IntegrityError as exc:
            raise DangerousGoodConflict(
                f"numer UN {draft.un_number} już istnieje"
            ) from exc

    @staticmethod
    def _normalized_create_inputs(
        *,
        un_number: str,
        imdg_class: str,
        name: str,
        aliases: list[str],
        adr_tunnel_code: str,
        segregation_group: str,
        packing_group: str,
        marine_pollutant: bool,
        limited_quantity: bool,
    ) -> _NormalizedGood:
        token = normalize_un_number(un_number)
        alias_tokens = normalize_un_aliases(aliases)
        if token in alias_tokens:
            raise InvalidDangerousGood("alias nie może powielać numeru UN")
        label = name.strip()
        if label == "":
            raise InvalidDangerousGood("nazwa towaru niebezpiecznego jest wymagana")
        return _NormalizedGood(
            un_number=token,
            imdg_class=normalize_imdg_class(imdg_class),
            adr_tunnel_code=normalize_adr_tunnel_code(adr_tunnel_code),
            segregation_group=normalize_segregation_group(segregation_group),
            packing_group=normalize_packing_group(packing_group),
            marine_pollutant=require_marine_pollutant(marine_pollutant),
            limited_quantity=require_limited_quantity(limited_quantity),
            name=label,
            aliases=alias_tokens,
        )

    async def resolve(self, raw: str) -> DangerousGood:
        token = normalize_un_number(raw)
        found = await self._goods.find_by_token(token)
        if found is None:
            raise UnknownDangerousGood(f"nieznany numer UN: {token}")
        return found

    async def _reject_taken(self, tokens: list[str]) -> None:
        for token in tokens:
            existing = await self._goods.find_by_token(token)
            if existing is not None:
                raise DangerousGoodConflict(f"numer UN {token} już istnieje")
