import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class DelayForecast(Base, TimestampMixin):
    __tablename__ = "delay_forecast"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_delay_forecast_org_id"),
        UniqueConstraint(
            "organization_id",
            "forecast_code",
            name="uq_delay_forecast_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_delay_forecast_org_source_ref",
        ),
        CheckConstraint(
            "forecast_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_delay_forecast_code",
        ),
        CheckConstraint(
            "horizon_hours BETWEEN 1 AND 168",
            name="ck_delay_forecast_horizon",
        ),
        CheckConstraint(
            "p_late >= 0 AND p_late <= 1",
            name="ck_delay_forecast_p_late",
        ),
        Index("ix_delay_forecast_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: prognoza opóźnienia HITL tego tenanta — p_late to dana, nie wróżba.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    forecast_code: Mapped[str] = mapped_column(String(32), nullable=False)
    horizon_hours: Mapped[int] = mapped_column(Integer(), nullable=False)
    p_late: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
