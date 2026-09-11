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


class Shipment(Base, TimestampMixin):
    __tablename__ = "shipment"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_shipment_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "quotation_id",
            name="uq_shipment_org_quotation",
        ),
        UniqueConstraint(
            "organization_id",
            "shipment_ref",
            name="uq_shipment_org_shipment_ref",
        ),
        CheckConstraint("status = 'draft'", name="ck_shipment_status_draft"),
        ForeignKeyConstraint(
            ["organization_id", "quotation_id"],
            ["quotation.organization_id", "quotation.id"],
            name="fk_shipment_quotation",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_shipment_party",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "parent_shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_shipment_parent",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "(parent_shipment_id IS NULL AND relation_kind IS NULL) OR "
            "(parent_shipment_id IS NOT NULL AND relation_kind IS NOT NULL AND "
            "relation_kind IN "
            "('drayage', 'oncarriage', 'leg_subcontract', 'other'))",
            name="ck_shipment_parent_pair",
        ),
        CheckConstraint(
            "parent_shipment_id IS NULL OR parent_shipment_id <> id",
            name="ck_shipment_parent_not_self",
        ),
        CheckConstraint(
            "guide_code IS NULL OR guide_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_shipment_guide_code",
        ),
        CheckConstraint(
            "plant_label IS NULL OR char_length(btrim(plant_label)) BETWEEN 1 AND 128",
            name="ck_shipment_plant_label",
        ),
        CheckConstraint(
            "carrier_label IS NULL OR char_length(btrim(carrier_label)) BETWEEN 1 AND 128",
            name="ck_shipment_carrier_label",
        ),
        Index("ix_shipment_org_party", "organization_id", "party_id"),
        Index("ix_shipment_org_created", "organization_id", "created_at"),
        Index("ix_shipment_org_parent", "organization_id", "parent_shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    # HITL twardy numer wydruku — nie QR i nie generator GD/2026.
    shipment_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    # HITL rodzic tego samego tenanta — nie widok marży na charge.
    parent_shipment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    relation_kind: Mapped[str | None] = mapped_column(String(32), nullable=True)
    guide_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    plant_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    carrier_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
