import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TelematicsDevice(Base, TimestampMixin):
    __tablename__ = "telematics_device"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_telematics_device_org_id"),
        UniqueConstraint(
            "organization_id",
            "device_code",
            name="uq_telematics_device_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_telematics_device_org_source_ref",
        ),
        CheckConstraint(
            "device_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_telematics_device_code",
        ),
        CheckConstraint(
            "device_kind IN ('tracker', 'fault', 'other')",
            name="ck_telematics_device_kind",
        ),
        Index("ix_telematics_device_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: urzadzenie tego tenanta — katalog HITL, nie live poll.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    device_code: Mapped[str] = mapped_column(String(32), nullable=False)
    device_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
