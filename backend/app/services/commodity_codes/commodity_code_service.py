from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.commodity_code import normalize_commodity_aliases, normalize_commodity_code
from app.domain.errors import CommodityCodeConflict, InvalidCommodityCode, UnknownCommodityCode
from app.models.commodity_code import CommodityCode
from app.repositories.commodity_codes.commodity_code_repository import CommodityCodeRepository

_MANUAL = "tenant:manual"


class CommodityCodeService:
    def __init__(self, session: AsyncSession) -> None:
        self._codes = CommodityCodeRepository(session)

    async def list_codes(self) -> list[CommodityCode]:
        return await self._codes.list_all()

    async def create_code(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
        aliases: list[str],
    ) -> CommodityCode:
        token = normalize_commodity_code(code)
        alias_tokens = normalize_commodity_aliases(aliases)
        if token in alias_tokens:
            raise InvalidCommodityCode("alias nie może powielać kodu")
        label = name.strip()
        if label == "":
            raise InvalidCommodityCode("nazwa kodu towarowego jest wymagana")
        await self._reject_taken([token, *alias_tokens])
        row = CommodityCode(
            id=uuid4(),
            organization_id=organization_id,
            code=token,
            name=label,
            aliases=alias_tokens,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._codes.add(row)
        except IntegrityError as exc:
            raise CommodityCodeConflict(f"kod towarowy {token} już istnieje") from exc

    async def get_code(self, code_id: UUID) -> CommodityCode:
        found = await self._codes.get(code_id)
        if found is None:
            raise UnknownCommodityCode(f"nieznany kod towarowy: {code_id}")
        return found

    async def resolve(self, raw: str) -> CommodityCode:
        token = normalize_commodity_code(raw)
        found = await self._codes.find_by_token(token)
        if found is None:
            raise UnknownCommodityCode(f"nieznany kod towarowy: {token}")
        return found

    async def _reject_taken(self, tokens: list[str]) -> None:
        for token in tokens:
            existing = await self._codes.find_by_token(token)
            if existing is not None:
                raise CommodityCodeConflict(f"kod towarowy {token} już istnieje")
