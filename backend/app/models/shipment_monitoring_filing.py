import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ShipmentMonitoringFiling(Base, TimestampMixin):
    __tablename__ = "shipment_monitoring_filing"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_shipment_monitoring_filing_org_id"),
        UniqueConstraint(
            "organization_id",
            "filing_code",
            name="uq_shipment_monitoring_filing_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_shipment_monitoring_filing_org_source_ref",
        ),
        CheckConstraint(
            "filing_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipment_monitoring_filing_code",
        ),
        CheckConstraint(
            "status_kind IN ('open', 'filed', 'closed', 'other')",
            name="ck_shipment_monitoring_filing_status_kind",
        ),
        Index("ix_shipment_monitoring_filing_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: stancja zgloszenia SENT/BDO — katalog HITL, nie live PUESC.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    filing_code: Mapped[str] = mapped_column(String(32), nullable=False)
    status_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
