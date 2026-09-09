from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_template import (
    require_member_code,
    require_template_code,
    require_template_source_ref,
    require_validity_window,
)
from app.domain.errors import InvalidChargeTemplate
from app.models.charge_template import ChargeTemplate
from app.repositories.charge_codes.charge_code_repository import ChargeCodeRepository
from app.repositories.charge_templates.charge_template_repository import ChargeTemplateRepository

_SPAN_CONSTRAINT = "ex_charge_template_no_overlap"


class ChargeTemplateService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ChargeTemplateRepository(session)
        self._codes = ChargeCodeRepository(session)

    async def list_templates(self) -> list[ChargeTemplate]:
        return await self._rows.list_all()

    async def record_template(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        template_code: object,
        charge_code: object,
        valid_from: object,
        valid_until: object,
        source_ref: object,
    ) -> ChargeTemplate:
        token = require_member_code(charge_code)
        found = await self._codes.find_by_token(token)
        if found is None:
            raise InvalidChargeTemplate("nieznany kod opłaty")
        start, end = require_validity_window(valid_from, valid_until)
        row = ChargeTemplate(
            id=uuid4(),
            organization_id=organization_id,
            template_code=require_template_code(template_code),
            charge_code=found.code,
            valid_from=start,
            valid_until=end,
            source_ref=require_template_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as exc:
            blob = f"{exc} {exc.orig}"
            if _SPAN_CONSTRAINT in blob:
                raise InvalidChargeTemplate("nakładanie okna ważności szablonu") from exc
            raise
