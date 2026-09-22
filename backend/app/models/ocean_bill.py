import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OceanBill(Base, TimestampMixin):
    __tablename__ = "ocean_bill"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_ocean_bill_shipment",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_ocean_bill_org_id"),
        CheckConstraint(
            "bill_kind IN ('hbl','mbl')",
            name="ck_ocean_bill_kind",
        ),
        Index("ix_ocean_bill_org_shipment", "organization_id", "shipment_id"),
        Index(
            "uq_ocean_bill_org_bill_no",
            "organization_id",
            "bill_no",
            unique=True,
            postgresql_where=text("bill_no IS NOT NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: konosament i zlecenie jednego tenanta — złożone FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    bill_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    bill_kind: Mapped[str] = mapped_column(String(8), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
