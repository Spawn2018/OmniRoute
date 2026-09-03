import uuid
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_LANE_PARTY_SQL = (
    "(origin_port_id IS NULL AND destination_port_id IS NULL AND party_id IS NULL) OR "
    "(origin_port_id IS NOT NULL AND destination_port_id IS NOT NULL AND party_id IS NOT NULL)"
)


class Quotation(Base, TimestampMixin):
    __tablename__ = "quotation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "origin_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_quotation_origin_port",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "destination_port_id"],
            ["port.organization_id", "port.id"],
            name="fk_quotation_destination_port",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_quotation_party",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "customer_rfq_id"],
            ["customer_rfq.organization_id", "customer_rfq.id"],
            name="fk_quotation_customer_rfq",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "commodity_code_id"],
            ["commodity_code.organization_id", "commodity_code.id"],
            name="fk_quotation_commodity_code",
            ondelete="RESTRICT",
        ),
        CheckConstraint(_LANE_PARTY_SQL, name="ck_quotation_lane_party_complete"),
        Index("ix_quotation_org_party_id", "organization_id", "party_id"),
        Index("ix_quotation_org_customer_rfq_id", "organization_id", "customer_rfq_id"),
        Index("ix_quotation_org_commodity_code_id", "organization_id", "commodity_code_id"),
        Index("ix_quotation_org_origin_port_id", "organization_id", "origin_port_id"),
        Index("ix_quotation_org_destination_port_id", "organization_id", "destination_port_id"),
        Index(
            "uq_quotation_org_document_number",
            "organization_id",
            "document_number",
            unique=True,
            postgresql_where=text("document_number IS NOT NULL"),
        ),
        Index(
            "ix_quotation_org_negotiated_channel",
            "organization_id",
            "negotiated_channel_quote_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    charge_code: Mapped[str] = mapped_column(String(32), nullable=False)
    rate_line_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rate_line.id", ondelete="RESTRICT"),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    origin_port_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    destination_port_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    party_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    customer_rfq_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    commodity_code_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    document_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    negotiated_channel_quote_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
