import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_KIND_SQL = (
    "question_kind IN ("
    "'loss','lane','risk','cash','other'"
    ")"
)


class ExecutiveMark(Base, TimestampMixin):
    __tablename__ = "executive_mark"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_executive_mark_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_executive_mark_org_source_ref",
        ),
        CheckConstraint(_KIND_SQL, name="ck_executive_mark_kind"),
        Index("ix_executive_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik pytania tego tenanta — HITL rodzaj, nie suma z modelu.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    question_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
