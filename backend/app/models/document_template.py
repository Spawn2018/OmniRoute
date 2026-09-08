import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class DocumentTemplate(Base, TimestampMixin):
    __tablename__ = "document_template"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_document_template_org_id"),
        CheckConstraint(
            "template_kind IN ('own_label','cmr')",
            name="ck_document_template_kind",
        ),
        CheckConstraint(
            "language IN ('pl','en')",
            name="ck_document_template_language",
        ),
        CheckConstraint(
            "output_kind IN ('html_print')",
            name="ck_document_template_output",
        ),
        Index("ix_document_template_org_kind", "organization_id", "template_kind"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: szablon wydruku jednego tenanta — CHECK kind nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    template_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    language: Mapped[str] = mapped_column(String(8), nullable=False)
    layout_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    output_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
