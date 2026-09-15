import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CfoNarrativeMark(Base, TimestampMixin):
    __tablename__ = "cfo_narrative_mark"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_cfo_narrative_mark_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_cfo_narrative_mark_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_cfo_narrative_mark_org_src",
        ),
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_cfo_narrative_mark_code",
        ),
        CheckConstraint(
            "narrative_kind IN ('anomaly', 'story', 'summary', 'other')",
            name="ck_cfo_narrative_mark_kind",
        ),
        Index("ix_cfo_narrative_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: etykieta narracji CFO — HITL, nie silnik narracji.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    narrative_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
