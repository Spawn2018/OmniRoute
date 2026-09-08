import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class OrganizationCalendar(Base, TimestampMixin):
    __tablename__ = "organization_calendar"
    __table_args__ = (
        CheckConstraint(
            "country_code ~ '^[A-Z]{2}$'",
            name="ck_organization_calendar_country",
        ),
        CheckConstraint(
            "day_kind IN ('holiday', 'working')",
            name="ck_organization_calendar_kind",
        ),
        Index(
            "ix_organization_calendar_org_country_day",
            "organization_id",
            "country_code",
            "calendar_day",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    calendar_day: Mapped[date] = mapped_column(Date, nullable=False)
    day_kind: Mapped[str] = mapped_column(String(8), nullable=False)
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization_calendar.id", ondelete="RESTRICT"),
        nullable=True,
    )
