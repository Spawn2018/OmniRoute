from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.model_feature_mark import parse_model_feature_mark_row
from app.models.model_feature_mark import ModelFeatureMark
from app.repositories.model_feature_marks.model_feature_mark_repository import (
    ModelFeatureMarkRepository,
)


class ModelFeatureMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ModelFeatureMarkRepository(session)

    async def list_marks(self) -> list[ModelFeatureMark]:
        return await self._rows.list_marks()

    async def persist_model_feature_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        feature_kind: object,
        source_ref: object,
    ) -> ModelFeatureMark:
        code, kind, origin = parse_model_feature_mark_row(
            mark_code,
            feature_kind,
            source_ref,
        )
        row = ModelFeatureMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            feature_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
