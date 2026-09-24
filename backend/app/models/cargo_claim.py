import uuid
from datetime import date

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CargoClaim(Base, TimestampMixin):
    __tablename__ = "cargo_claim"
    __table_args__ = (
        CheckConstraint(
            "claim_kind IN ('damage', 'shortage', 'other')",
            name="ck_cargo_claim_kind",
        ),
        CheckConstraint(
            "damage_code IN ('overage', 'shortage', 'damage', 'loss')",
            name="ck_cargo_claim_damage_code",
        ),
        CheckConstraint(
            "cmr_notice_window IN ('notice_7', 'notice_21')",
            name="ck_cargo_claim_cmr_notice_window",
        ),
        CheckConstraint(
            "suit_due_at >= notice_due_at",
            name="ck_cargo_claim_cmr_order",
        ),
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_cargo_claim_shipment",
            ondelete="RESTRICT",
        ),
        Index("ix_cargo_claim_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: reklamacja należy do tenanta zlecenia — złożone FK nie zastępują current_org.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    claim_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    damage_code: Mapped[str] = mapped_column(String(16), nullable=False)
    cmr_notice_window: Mapped[str] = mapped_column(String(16), nullable=False)
    notice_due_at: Mapped[date] = mapped_column(Date, nullable=False)
    suit_due_at: Mapped[date] = mapped_column(Date, nullable=False)
    evidence_gps: Mapped[bool] = mapped_column(Boolean, nullable=False)
    evidence_temp: Mapped[bool] = mapped_column(Boolean, nullable=False)
    evidence_photo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
