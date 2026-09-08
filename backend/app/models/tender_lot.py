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


class TenderLot(Base, TimestampMixin):
    __tablename__ = "tender_lot"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tender_lot_org_id"),
        UniqueConstraint(
            "organization_id",
            "tender_id",
            "lot_code",
            name="uq_tender_lot_org_tender_code",
        ),
        CheckConstraint("char_length(btrim(lot_code)) > 0", name="ck_tender_lot_code"),
        ForeignKeyConstraint(
            ["organization_id", "tender_id"],
            ["tender.organization_id", "tender.id"],
            name="fk_tender_lot_tender",
            ondelete="RESTRICT",
        ),
        Index("ix_tender_lot_org_tender", "organization_id", "tender_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    lot_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
