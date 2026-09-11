import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ClauseNotice(Base, TimestampMixin):
    __tablename__ = "clause_notice"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_clause_notice_org_id"),
        UniqueConstraint(
            "organization_id",
            "notice_code",
            name="uq_clause_notice_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_clause_notice_org_source_ref",
        ),
        CheckConstraint(
            "notice_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_clause_notice_code",
        ),
        CheckConstraint(
            "char_length(btrim(clause_label)) BETWEEN 1 AND 128",
            name="ck_clause_notice_clause_label",
        ),
        Index("ix_clause_notice_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: powiadomienie o klauzuli HITL tego tenanta — etykieta, nie FK sla_clause.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    notice_code: Mapped[str] = mapped_column(String(32), nullable=False)
    clause_label: Mapped[str] = mapped_column(String(128), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
