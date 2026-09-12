import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class EccnMark(Base, TimestampMixin):
    __tablename__ = "eccn_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_eccn_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_eccn_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_eccn_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_eccn_mark_code",
        ),
        CheckConstraint(
            "control_kind IN ('eccn', 'ear', 'license', 'other')",
            name="ck_eccn_mark_control_kind",
        ),
        Index("ix_eccn_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik MQC tego tenanta — katalog HITL, nie live giełda hubu.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    control_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
