import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class HandoverSbarMark(Base, TimestampMixin):
    __tablename__ = "handover_sbar_mark"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_handover_sbar_mark_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_handover_sbar_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_handover_sbar_mark_org_src",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_handover_sbar_mark_code",
        ),
        CheckConstraint(
            "sbar_kind IN ("
            "'situation', 'background', 'assessment', 'recommendation', 'other'"
            ")",
            name="ck_handover_sbar_mark_kind",
        ),
        Index("ix_handover_sbar_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: przekazanie zmiany SBAR — HITL, nie drugi czat.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    sbar_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
