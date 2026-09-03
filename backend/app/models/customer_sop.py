import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CustomerSop(Base, TimestampMixin):
    __tablename__ = "customer_sop"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "party_id",
            "code",
            name="uq_customer_sop_org_party_code",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_customer_sop_party",
            ondelete="RESTRICT",
        ),
        CheckConstraint("code ~ '^[a-z][a-z0-9_]{1,31}$'", name="ck_customer_sop_code_snake"),
        CheckConstraint("status IN ('draft', 'approved')", name="ck_customer_sop_status"),
        CheckConstraint("char_length(body) >= 1", name="ck_customer_sop_body_len"),
        CheckConstraint(
            "(status = 'draft' AND approved_at IS NULL) OR "
            "(status = 'approved' AND approved_at IS NOT NULL)",
            name="ck_customer_sop_approved_pair",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(8), nullable=False, server_default=text("'draft'"))
    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    blocks_auto: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
