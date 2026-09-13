import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PoFinancingMark(Base, TimestampMixin):
    __tablename__ = "po_financing_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_po_financing_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_po_financing_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_po_financing_mark_org_src",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_po_financing_mark_code",
        ),
        CheckConstraint(
            "financing_kind IN ('po', 'release', 'advance', 'other')",
            name="ck_po_financing_mark_kind",
        ),
        Index("ix_po_financing_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: stance PO Financing tego tenanta — nie FK purchase_order i nie wycena zapasu.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    financing_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
