import uuid
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PortSurcharge(Base, TimestampMixin):
    __tablename__ = "port_surcharge"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "port_id",
            "code",
            name="uq_port_surcharge_org_port_code",
        ),
        ForeignKeyConstraint(
            ["organization_id", "port_id"],
            ["port.organization_id", "port.id"],
            name="fk_port_surcharge_port",
            ondelete="RESTRICT",
        ),
        CheckConstraint("code ~ '^[a-z][a-z0-9_]{1,31}$'", name="ck_port_surcharge_code_snake"),
        CheckConstraint("currency ~ '^[A-Z]{3}$'", name="ck_port_surcharge_currency_iso"),
        CheckConstraint("amount > 0", name="ck_port_surcharge_amount_positive"),
        CheckConstraint("char_length(title) >= 1", name="ck_port_surcharge_title_len"),
        CheckConstraint("char_length(applies_when) >= 1", name="ck_port_surcharge_when_len"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    port_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    applies_when: Mapped[str] = mapped_column(String(512), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
