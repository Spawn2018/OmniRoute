import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


class OutcomeLedger(Base, TimestampMixin):
    __tablename__ = "outcome_ledger"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_outcome_ledger_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_outcome_ledger_org_source_ref",
        ),
        ForeignKeyConstraint(
            ["organization_id", "outcome_kind"],
            ["outcome_kind.organization_id", "outcome_kind.kind_code"],
            name="fk_outcome_ledger_kind",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            f"target_bc ~ '{_SNAKE}'",
            name="ck_outcome_ledger_target_bc",
        ),
        Index("ix_outcome_ledger_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: ledger faktu tego tenanta — UUID podpowiedzi jest daną, nie FK.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    target_bc: Mapped[str] = mapped_column(String(32), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    suggestion_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    outcome_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    actual_value: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
