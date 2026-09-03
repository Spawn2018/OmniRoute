import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CustomerRfq(Base, TimestampMixin):
    __tablename__ = "customer_rfq"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_customer_rfq_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "inbound_message_id",
            name="uq_customer_rfq_org_message",
        ),
        CheckConstraint("status = 'draft'", name="ck_customer_rfq_status_draft"),
        CheckConstraint(
            "source_ref ~ '^(fixture|synth)://'",
            name="ck_customer_rfq_source_fixture",
        ),
        ForeignKeyConstraint(
            ["organization_id", "inbound_message_id"],
            ["inbound_message.organization_id", "inbound_message.id"],
            name="fk_customer_rfq_inbound_message",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_customer_rfq_party",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "commodity_code_id"],
            ["commodity_code.organization_id", "commodity_code.id"],
            name="fk_customer_rfq_commodity_code",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "dangerous_good_id"],
            ["dangerous_good.organization_id", "dangerous_good.id"],
            name="fk_customer_rfq_dangerous_good",
            ondelete="RESTRICT",
        ),
        Index("ix_customer_rfq_org_commodity_code_id", "organization_id", "commodity_code_id"),
        Index("ix_customer_rfq_org_dangerous_good_id", "organization_id", "dangerous_good_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    inbound_message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False)
    party_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    commodity_code_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    dangerous_good_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
