from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidGdprRequest, ResourceNotFound
from app.domain.gdpr_request import (
    require_gdpr_app_user_id,
    require_gdpr_request_kind,
    require_gdpr_request_source_ref,
    require_open_gdpr_request,
)
from app.models.gdpr_request import GdprRequest
from app.repositories.gdpr_requests.gdpr_request_repository import GdprRequestRepository


class GdprRequestService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = GdprRequestRepository(session)

    async def list_rows(self) -> list[GdprRequest]:
        return await self._rows.list_all()

    async def record_row(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        app_user_id: UUID,
        request_kind: str,
        source_ref: str,
    ) -> GdprRequest:
        row = GdprRequest(
            id=uuid4(),
            organization_id=organization_id,
            app_user_id=require_gdpr_app_user_id(app_user_id),
            request_kind=require_gdpr_request_kind(request_kind),
            status="open",
            source_ref=require_gdpr_request_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidGdprRequest("wniosek już otwarty") from orig

    async def fulfill(self, request_id: UUID) -> GdprRequest:
        row = await self._rows.get_by_id(request_id)
        if row is None:
            raise ResourceNotFound("nieznany wniosek")
        require_open_gdpr_request(row.status)
        row.status = "fulfilled"
        return row
