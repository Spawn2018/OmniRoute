import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class NctsDraft(Base, TimestampMixin):
    __tablename__ = "ncts_draft"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_ncts_draft_org_id"),
        UniqueConstraint(
            "organization_id",
            "draft_code",
            name="uq_ncts_draft_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_ncts_draft_org_source_ref",
        ),
        CheckConstraint(
            "draft_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_ncts_draft_code",
        ),
        CheckConstraint(
            "transit_kind IN ('t1', 't2', 'other')",
            name="ck_ncts_draft_transit_kind",
        ),
        Index("ix_ncts_draft_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: szkic NCTS tego tenanta — katalog HITL, nie PUESC.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    draft_code: Mapped[str] = mapped_column(String(32), nullable=False)
    transit_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
