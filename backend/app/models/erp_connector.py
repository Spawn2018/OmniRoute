import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ErpConnector(Base, TimestampMixin):
    __tablename__ = "erp_connector"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_erp_connector_org_id"),
        UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_erp_connector_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_erp_connector_org_source_ref",
        ),
        CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_erp_connector_code",
        ),
        CheckConstraint(
            "system_kind IN ('optima')",
            name="ck_erp_connector_kind",
        ),
        Index("ix_erp_connector_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: konektor Optima tego tenanta — kind to dana, nie live SOAP.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    connector_code: Mapped[str] = mapped_column(String(32), nullable=False)
    system_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
