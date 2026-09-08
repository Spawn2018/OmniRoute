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


class CodInstruction(Base, TimestampMixin):
    __tablename__ = "cod_instruction"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "shipment_id"],
            ["shipment.organization_id", "shipment.id"],
            name="fk_cod_instruction_shipment",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_cod_instruction_org_id"),
        CheckConstraint(
            "collection_status IN ('noted','advised','collected','refused')",
            name="ck_cod_instruction_status",
        ),
        Index("ix_cod_instruction_org_shipment", "organization_id", "shipment_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik COD i zlecenie jednego tenanta — złożone FK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    instruction_code: Mapped[str] = mapped_column(String(32), nullable=False)
    collection_status: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
