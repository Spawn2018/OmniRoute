import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PartyDocument(Base, TimestampMixin):
    __tablename__ = "party_document"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_party_document_org_id"),
        UniqueConstraint(
            "organization_id",
            "party_id",
            "document_kind",
            name="uq_party_document_org_party_kind",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_party_document_party",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "document_kind ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_party_document_kind",
        ),
        Index("ix_party_document_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: dokument kontrahenta tego tenanta — kind nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    document_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
