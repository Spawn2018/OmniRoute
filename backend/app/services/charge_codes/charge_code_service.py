from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_code import normalize_aliases, normalize_charge_code
from app.domain.errors import ChargeCodeConflict, InvalidChargeCode, UnknownChargeCode
from app.domain.rate_line import require_source_ref
from app.models.charge_code import ChargeCode
from app.repositories.charge_codes.charge_code_repository import ChargeCodeRepository


class ChargeCodeService:
    def __init__(self, session: AsyncSession) -> None:
        self._codes = ChargeCodeRepository(session)
        self._session = session

    async def list_codes(self) -> list[ChargeCode]:
        return await self._codes.list_all()

    async def create_code(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
        aliases: list[str],
        source_ref: str,
    ) -> ChargeCode:
        token = normalize_charge_code(code)
        alias_tokens = normalize_aliases(aliases)
        if token in alias_tokens:
            raise InvalidChargeCode("alias nie może powielać kodu")
        label = name.strip()
        if label == "":
            raise InvalidChargeCode("nazwa kodu opłaty jest wymagana")
        origin = require_source_ref(source_ref)
        await self._reject_taken([token, *alias_tokens])
        row = ChargeCode(
            id=uuid4(),
            organization_id=organization_id,
            code=token,
            name=label,
            aliases=alias_tokens,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._codes.add(row)
        except IntegrityError as exc:
            raise ChargeCodeConflict(f"kod opłaty {token} już istnieje") from exc

    async def resolve(self, raw: str) -> ChargeCode:
        token = normalize_charge_code(raw)
        found = await self._codes.find_by_token(token)
        if found is None:
            raise UnknownChargeCode(f"nieznany kod opłaty: {token}")
        return found

    async def _reject_taken(self, tokens: list[str]) -> None:
        for token in tokens:
            existing = await self._codes.find_by_token(token)
            if existing is not None:
                raise ChargeCodeConflict(f"kod opłaty {token} już istnieje")
