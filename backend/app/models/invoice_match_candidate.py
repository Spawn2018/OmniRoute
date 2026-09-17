import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class InvoiceMatchCandidate(Base, TimestampMixin):
    __tablename__ = "invoice_match_candidate"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_invoice_match_candidate_org_id"),
        UniqueConstraint(
            "organization_id",
            "candidate_code",
            name="uq_invoice_match_candidate_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_invoice_match_candidate_org_source_ref",
        ),
        CheckConstraint(
            "candidate_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_invoice_match_candidate_code",
        ),
        CheckConstraint(
            "candidate_kind IN ('proposed', 'held', 'rejected', 'other')",
            name="ck_invoice_match_candidate_candidate_kind",
        ),
        Index("ix_invoice_match_candidate_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: stancja kandydata dopasowania FV — katalog HITL, nie live ranking SQL.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    candidate_code: Mapped[str] = mapped_column(String(32), nullable=False)
    candidate_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
