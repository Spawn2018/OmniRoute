from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dangerous_good import (
    normalize_imdg_class,
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

    async def create_good(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        un_number: str,
        imdg_class: str,
        name: str,
        aliases: list[str],
    ) -> DangerousGood:
        token = normalize_un_number(un_number)
        klass = normalize_imdg_class(imdg_class)
        alias_tokens = normalize_un_aliases(aliases)
        if token in alias_tokens:
            raise InvalidDangerousGood("alias nie może powielać numeru UN")
        label = name.strip()
        if label == "":
            raise InvalidDangerousGood("nazwa towaru niebezpiecznego jest wymagana")
        await self._reject_taken([token, *alias_tokens])
        row = DangerousGood(
            id=uuid4(),
            organization_id=organization_id,
            un_number=token,
            imdg_class=klass,
            name=label,
            aliases=alias_tokens,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._goods.add(row)
        except IntegrityError as exc:
            raise DangerousGoodConflict(f"numer UN {token} już istnieje") from exc

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
