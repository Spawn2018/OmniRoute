import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_KIND_SQL = "exception_kind IN ('noted', 'blocked', 'other')"


class OperationalException(Base, TimestampMixin):
    __tablename__ = "operational_exception"
    __table_args__ = (
        CheckConstraint(_KIND_SQL, name="ck_operational_exception_kind"),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_operational_exception_shipment",
            ondelete="RESTRICT",
        ),
        Index("ix_operational_exception_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    exception_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
