import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_CONDITION_SQL = "condition_code IN ('clear','rain','snow','wind','fog','ice','other')"


class WeatherObservation(Base, TimestampMixin):
    __tablename__ = "weather_observation"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_weather_observation_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_weather_observation_org_source_ref",
        ),
        CheckConstraint(_CONDITION_SQL, name="ck_weather_observation_condition"),
        CheckConstraint(
            "station_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_weather_observation_station",
        ),
        CheckConstraint("provider_code = 'hitl'", name="ck_weather_observation_provider"),
        Index("ix_weather_observation_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: obserwacja pogody tego tenanta — HITL, nie feed.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    condition_code: Mapped[str] = mapped_column(String(8), nullable=False)
    station_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    provider_code: Mapped[str] = mapped_column(String(8), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
