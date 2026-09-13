import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"
_CCY = r"^[A-Z]{3}$"


class BenefitLedger(Base, TimestampMixin):
    __tablename__ = "benefit_ledger"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_benefit_ledger_org_id"),
        UniqueConstraint(
            "organization_id",
            "benefit_code",
            name="uq_benefit_ledger_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_benefit_ledger_org_source_ref",
        ),
        CheckConstraint(
            f"benefit_code ~ '{_SNAKE}'",
            name="ck_benefit_ledger_code",
        ),
        CheckConstraint(
            f"saved_currency ~ '{_CCY}'",
            name="ck_benefit_ledger_currency",
        ),
        Index("ix_benefit_ledger_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: ledger oszczędności tego tenanta — metoda i kwota są danymi HITL.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    benefit_code: Mapped[str] = mapped_column(String(32), nullable=False)
    method_label: Mapped[str] = mapped_column(String(256), nullable=False)
    hours_saved: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    saved_amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    saved_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
