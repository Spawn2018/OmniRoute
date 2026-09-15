from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.model_feature_mark import ModelFeatureMark


class ModelFeatureMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ModelFeatureMark]:
        stmt = select(ModelFeatureMark).order_by(
            ModelFeatureMark.mark_code,
            ModelFeatureMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: ModelFeatureMark) -> ModelFeatureMark:
        self._session.add(row)
        await self._session.flush()
        return row
