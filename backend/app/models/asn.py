import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Asn(Base, TimestampMixin):
    __tablename__ = "asn"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "purchase_order_id"],
            ["purchase_order.organization_id", "purchase_order.id"],
            name="fk_asn_purchase_order",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_asn_org_id"),
        UniqueConstraint(
            "organization_id",
            "purchase_order_id",
            "asn_code",
            name="uq_asn_org_header_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_asn_org_source_ref",
        ),
        CheckConstraint(
            "asn_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_asn_code",
        ),
        CheckConstraint(
            "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
            name="ck_asn_plant",
        ),
        CheckConstraint(
            "carrier_label IS NULL OR char_length(btrim(carrier_label)) BETWEEN 1 AND 128",
            name="ck_asn_carrier",
        ),
        CheckConstraint(
            "ship_ref_label IS NULL OR char_length(btrim(ship_ref_label)) BETWEEN 1 AND 128",
            name="ck_asn_ship_ref",
        ),
        Index("ix_asn_organization_id", "organization_id"),
        Index("ix_asn_org_header", "organization_id", "purchase_order_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: awizo HITL tego tenanta — nie EDI live i nie shipment.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    purchase_order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    asn_code: Mapped[str] = mapped_column(String(32), nullable=False)
    plant_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    carrier_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    ship_ref_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
