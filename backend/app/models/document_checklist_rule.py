import uuid

from sqlalchemy import (
    CHAR,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class DocumentChecklistRule(Base, TimestampMixin):
    __tablename__ = "document_checklist_rule"
    __table_args__ = (
        CheckConstraint(
            "incoterm IN ('EXW','FCA','CPT','CIP','DAP','DPU','DDP','FAS','FOB','CFR','CIF')",
            name="ck_document_checklist_rule_incoterm",
        ),
        CheckConstraint(
            "trade_side IN ('import', 'export')",
            name="ck_document_checklist_rule_side",
        ),
        CheckConstraint(
            "mode IN ('ocean', 'road', 'rail', 'air')",
            name="ck_document_checklist_rule_mode",
        ),
        CheckConstraint(
            "document_kind IN ("
            "'commercial_invoice', 'packing_list', 'bill_of_lading', 'export_declaration')",
            name="ck_document_checklist_rule_kind",
        ),
        UniqueConstraint(
            "organization_id",
            "incoterm",
            "trade_side",
            "mode",
            "document_kind",
            name="uq_document_checklist_rule_triple_kind",
        ),
        Index(
            "ix_document_checklist_rule_org_triple",
            "organization_id",
            "incoterm",
            "trade_side",
            "mode",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    incoterm: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    trade_side: Mapped[str] = mapped_column(String(6), nullable=False)
    mode: Mapped[str] = mapped_column(String(8), nullable=False)
    document_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    blocks_dispatch: Mapped[bool] = mapped_column(Boolean, nullable=False)
