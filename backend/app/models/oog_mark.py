import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OogMark(Base, TimestampMixin):
    __tablename__ = "oog_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_oog_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_oog_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_oog_mark_org_source_ref",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_oog_mark_code",
        ),
        CheckConstraint(
            "escort_kind IN ('oog', 'lashing', 'escort', 'other')",
            name="ck_oog_mark_escort_kind",
        ),
        Index("ix_oog_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik OOG tego tenanta — katalog HITL, nie wymiary.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    escort_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
