import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"
_CCY = r"^[A-Z]{3}$"
_UNLO = r"^[A-Z]{2}[A-Z0-9]{3}$"


class MarginFloor(Base, TimestampMixin):
    __tablename__ = "margin_floor"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_margin_floor_org_id"),
        UniqueConstraint(
            "organization_id",
            "floor_code",
            name="uq_margin_floor_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_margin_floor_org_source_ref",
        ),
        CheckConstraint(
            f"floor_code ~ '{_SNAKE}'",
            name="ck_margin_floor_code",
        ),
        CheckConstraint(
            f"floor_currency ~ '{_CCY}'",
            name="ck_margin_floor_currency",
        ),
        CheckConstraint(
            f"origin_unlocode ~ '{_UNLO}'",
            name="ck_margin_floor_origin_unlocode",
        ),
        CheckConstraint(
            f"destination_unlocode ~ '{_UNLO}'",
            name="ck_margin_floor_destination_unlocode",
        ),
        CheckConstraint(
            "origin_unlocode <> destination_unlocode",
            name="ck_margin_floor_unlocode_pair",
        ),
        Index("ix_margin_floor_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: podłoga marży tego tenanta — HITL Decimal; 409 = API charges (539.0).
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    floor_code: Mapped[str] = mapped_column(String(32), nullable=False)
    origin_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    destination_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    floor_amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    floor_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
