import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OrganizationSetting(Base, TimestampMixin):
    __tablename__ = "organization_setting"
    __table_args__ = (
        UniqueConstraint("organization_id", "setting_key", name="uq_organization_setting_org_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    setting_key: Mapped[str] = mapped_column(String(64), nullable=False)
    setting_value: Mapped[str] = mapped_column(String(64), nullable=False)
