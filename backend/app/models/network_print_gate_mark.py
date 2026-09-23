import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class NetworkPrintGateMark(Base, TimestampMixin):
    __tablename__ = "network_print_gate_mark"
    __table_args__ = (
        CheckConstraint(
            "mark_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_network_print_gate_mark_code",
        ),
        CheckConstraint(
            "gate_kind IN ('block_409', 'warn_only', 'record_only', 'other')",
            name="ck_network_print_gate_mark_kind",
        ),
        UniqueConstraint(
            "organization_id", "id", name="uq_network_print_gate_mark_org_id"
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_network_print_gate_mark_org_source_ref",
        ),
        UniqueConstraint(
            "organization_id",
            "mark_code",
            name="uq_network_print_gate_mark_org_code",
        ),
        Index("ix_network_print_gate_mark_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: stance bramy wydruku sieci — HITL, nie live 409.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    mark_code: Mapped[str] = mapped_column(String(32), nullable=False)
    gate_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
