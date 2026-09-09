import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class MonitoringScheme(Base, TimestampMixin):
    __tablename__ = "monitoring_scheme"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_monitoring_scheme_org_id"),
        UniqueConstraint(
            "organization_id",
            "scheme_code",
            name="uq_monitoring_scheme_org_code",
        ),
        CheckConstraint(
            "scheme_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_monitoring_scheme_code",
        ),
        Index("ix_monitoring_scheme_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: schemat monitoringu tego tenanta — kod nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    scheme_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
