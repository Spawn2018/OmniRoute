import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CarbonMethod(Base, TimestampMixin):
    __tablename__ = "carbon_method"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_carbon_method_org_id"),
        UniqueConstraint(
            "organization_id",
            "method_code",
            "method_version",
            name="uq_carbon_method_org_code_version",
        ),
        CheckConstraint(
            "method_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_carbon_method_code",
        ),
        CheckConstraint(
            "method_version ~ '^[a-z0-9][a-z0-9_]{0,31}$'",
            name="ck_carbon_method_version",
        ),
        Index("ix_carbon_method_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: metodyka CO2 tego tenanta — kod nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    method_code: Mapped[str] = mapped_column(String(32), nullable=False)
    method_version: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
