import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_KIND_SQL = "prediction_kind IN ('eta','transit','disrupt')"
_HORIZON_SQL = "horizon_code IN ('h1h','h6h','h24h','h7d')"


class PredictionLedger(Base, TimestampMixin):
    __tablename__ = "prediction_ledger"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_prediction_ledger_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_prediction_ledger_org_source_ref",
        ),
        CheckConstraint(_KIND_SQL, name="ck_prediction_ledger_kind"),
        CheckConstraint(_HORIZON_SQL, name="ck_prediction_ledger_horizon"),
        CheckConstraint("crps >= 0", name="ck_prediction_ledger_crps"),
        CheckConstraint("mae >= 0", name="ck_prediction_ledger_mae"),
        CheckConstraint("interval_high >= interval_low", name="ck_prediction_ledger_interval"),
        CheckConstraint(
            "model_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_prediction_ledger_model",
        ),
        Index("ix_prediction_ledger_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: ledger predykcji tego tenanta — CRPS w CHECK nie zastępuje polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    prediction_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    horizon_code: Mapped[str] = mapped_column(String(8), nullable=False)
    interval_low: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    interval_high: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    crps: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    mae: Mapped[Decimal | None] = mapped_column(Numeric(14, 4), nullable=True)
    model_code: Mapped[str] = mapped_column(String(32), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
