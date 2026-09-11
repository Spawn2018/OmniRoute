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


class RemediationOption(Base, TimestampMixin):
    __tablename__ = "remediation_option"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_remediation_option_org_id"),
        UniqueConstraint(
            "organization_id",
            "option_code",
            name="uq_remediation_option_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_remediation_option_org_source_ref",
        ),
        CheckConstraint(
            "option_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_remediation_option_code",
        ),
        CheckConstraint(
            "option_kind IN ('rebook', 'wait', 'claim', 'other')",
            name="ck_remediation_option_kind",
        ),
        Index("ix_remediation_option_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: opcja naprawy HITL tego tenanta — kind jako dana, nie kwota.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    option_code: Mapped[str] = mapped_column(String(32), nullable=False)
    option_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
