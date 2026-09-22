from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.document_template import (
    require_branding_ref,
    require_layout_ref,
    require_output_kind,
    require_template_kind,
    require_template_language,
    require_template_source_ref,
)
from app.models.document_template import DocumentTemplate
from app.repositories.document_templates.document_template_repository import (
    DocumentTemplateRepository,
)


class DocumentTemplateService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = DocumentTemplateRepository(session)

    async def list_templates(self) -> list[DocumentTemplate]:
        return await self._rows.list_all()

    async def record_template(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        template_kind: object,
        language: object,
        layout_ref: object,
        output_kind: object,
        source_ref: object,
        branding_ref: object = None,
    ) -> DocumentTemplate:
        row = DocumentTemplate(
            id=uuid4(),
            organization_id=organization_id,
            template_kind=require_template_kind(template_kind),
            language=require_template_language(language),
            layout_ref=require_layout_ref(layout_ref),
            branding_ref=require_branding_ref(branding_ref),
            output_kind=require_output_kind(output_kind),
            source_ref=require_template_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
