import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PoPlantMark(Base, TimestampMixin):
    __tablename__ = "po_plant_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_po_plant_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_po_plant_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_po_plant_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_po_plant_mark_code",
        ),
        CheckConstraint(
            "plant_kind IN ('plant', 'batch', 'sku', 'other')",
            name="ck_po_plant_mark_plant_kind",
        ),
        Index("ix_po_plant_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik plant/batch/SKU tego tenanta — katalog HITL, nie live EDI.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    plant_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
