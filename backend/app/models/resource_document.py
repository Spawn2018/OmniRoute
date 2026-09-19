import uuid
from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ResourceDocument(Base, TimestampMixin):
    __tablename__ = "resource_document"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_resource_document_org_id"),
        ForeignKeyConstraint(
            ["organization_id", "resource_id"],
            ["resource.organization_id", "resource.id"],
            name="fk_resource_document_resource",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "document_kind IN ('licence', 'insurance', 'other')",
            name="ck_resource_document_kind",
        ),
        Index("ix_resource_document_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: waznosc floty tego tenanta — party_document to inny podmiot.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    document_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
