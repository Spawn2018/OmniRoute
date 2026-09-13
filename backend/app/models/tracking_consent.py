import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TrackingConsent(Base, TimestampMixin):
    __tablename__ = "tracking_consent"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tracking_consent_org_id"),
        UniqueConstraint(
            "organization_id",
            "consent_code",
            name="uq_tracking_consent_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tracking_consent_org_source_ref",
        ),
        CheckConstraint(
            "consent_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tracking_consent_code",
        ),
        CheckConstraint(
            "consent_kind IN ('party', 'driver', 'other')",
            name="ck_tracking_consent_kind",
        ),
        Index("ix_tracking_consent_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: zgoda tego tenanta — katalog HITL, nie kolumna na kontakcie.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    consent_code: Mapped[str] = mapped_column(String(32), nullable=False)
    consent_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
