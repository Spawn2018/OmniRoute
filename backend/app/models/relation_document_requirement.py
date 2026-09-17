import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class RelationDocumentRequirement(Base, TimestampMixin):
    __tablename__ = "relation_document_requirement"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_relation_document_requirement_org_id"),
        UniqueConstraint(
            "organization_id",
            "requirement_code",
            name="uq_relation_document_requirement_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_relation_document_requirement_org_source_ref",
        ),
        CheckConstraint(
            "requirement_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_relation_document_requirement_code",
        ),
        CheckConstraint(
            "relation_kind IN ('domestic', 'international', 'waste', 'other')",
            name="ck_relation_document_requirement_relation_kind",
        ),
        Index("ix_relation_document_requirement_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: stancja wymogu dokumentow relacji — katalog HITL, nie live 409 na shipment.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    requirement_code: Mapped[str] = mapped_column(String(32), nullable=False)
    relation_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
