import uuid

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class DocumentDispatchRule(Base, TimestampMixin):
    __tablename__ = "document_dispatch_rule"
    __table_args__ = (
        CheckConstraint(
            "incoterm IN ('EXW','FCA','CPT','CIP','DAP','DPU','DDP','FAS','FOB','CFR','CIF')",
            name="ck_document_dispatch_rule_incoterm",
        ),
        CheckConstraint(
            "trade_side IN ('import', 'export')",
            name="ck_document_dispatch_rule_side",
        ),
        CheckConstraint(
            "document_kind IN ("
            "'commercial_invoice', 'packing_list', 'bill_of_lading', 'export_declaration')",
            name="ck_document_dispatch_rule_kind",
        ),
        CheckConstraint(
            "recipient_role IN ("
            "'shipper','consignee','origin_agent','dest_agent',"
            "'ocean_carrier','omni_customs','client_customs')",
            name="ck_document_dispatch_rule_role",
        ),
        Index(
            "ix_document_dispatch_rule_org_triple",
            "organization_id",
            "incoterm",
            "trade_side",
            "document_kind",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("document_dispatch_rule.id", ondelete="RESTRICT"),
        nullable=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    recipient_role: Mapped[str] = mapped_column(String(20), nullable=False)
    document_kind: Mapped[str] = mapped_column(String(24), nullable=False)
    trade_side: Mapped[str] = mapped_column(String(8), nullable=False)
    incoterm: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
