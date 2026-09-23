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
)
from app.domain.errors import (
    DangerousGoodConflict,
    InvalidDangerousGood,
    UnknownDangerousGood,
)
from app.models.dangerous_good import DangerousGood
from app.repositories.dangerous_goods.dangerous_good_repository import DangerousGoodRepository

_MANUAL = "tenant:manual"


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
    ) -> DangerousGood:
        token, klass, tunnel, group, packing, label, alias_tokens = (
            self._normalized_create_inputs(
                un_number=un_number,
                imdg_class=imdg_class,
                name=name,
                aliases=aliases,
                adr_tunnel_code=adr_tunnel_code,
                segregation_group=segregation_group,
                packing_group=packing_group,
            )
        )
        await self._reject_taken([token, *alias_tokens])
        return await self._insert_good(
            organization_id=organization_id,
            user_id=user_id,
            un_number=token,
            imdg_class=klass,
            adr_tunnel_code=tunnel,
            segregation_group=group,
            packing_group=packing,
            name=label,
            aliases=alias_tokens,
        )

    async def _insert_good(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        un_number: str,
        imdg_class: str,
        adr_tunnel_code: str,
        segregation_group: str,
        packing_group: str,
        name: str,
        aliases: list[str],
    ) -> DangerousGood:
        row = DangerousGood(
            id=uuid4(),
            organization_id=organization_id,
            un_number=un_number,
            imdg_class=imdg_class,
            adr_tunnel_code=adr_tunnel_code,
            segregation_group=segregation_group,
            packing_group=packing_group,
            name=name,
            aliases=aliases,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._goods.add(row)
        except IntegrityError as exc:
            raise DangerousGoodConflict(f"numer UN {un_number} już istnieje") from exc

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
    ) -> tuple[str, str, str, str, str, str, list[str]]:
        token = normalize_un_number(un_number)
        alias_tokens = normalize_un_aliases(aliases)
        if token in alias_tokens:
            raise InvalidDangerousGood("alias nie może powielać numeru UN")
        label = name.strip()
        if label == "":
            raise InvalidDangerousGood("nazwa towaru niebezpiecznego jest wymagana")
        return (
            token,
            normalize_imdg_class(imdg_class),
            normalize_adr_tunnel_code(adr_tunnel_code),
            normalize_segregation_group(segregation_group),
            normalize_packing_group(packing_group),
            label,
            alias_tokens,
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
