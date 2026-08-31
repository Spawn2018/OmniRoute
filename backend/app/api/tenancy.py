from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_tenant_session
from app.services.tenancy.service import TenancyService


class AppUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    email: EmailStr
    display_name: str


router = APIRouter(prefix="/tenancy", tags=["tenancy"])


@router.get("/users", response_model=list[AppUserResponse])
async def list_users(
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AppUserResponse]:
    service = TenancyService(session)
    users = await service.list_users()
    return [AppUserResponse.model_validate(user) for user in users]
