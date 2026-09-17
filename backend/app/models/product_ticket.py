import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ProductTicket(Base, TimestampMixin):
    __tablename__ = "product_ticket"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_product_ticket_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "ticket_code",
            name="uq_product_ticket_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_product_ticket_org_src",
        ),
        CheckConstraint(
            "ticket_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_product_ticket_code",
        ),
        CheckConstraint(
            "char_length(title) BETWEEN 1 AND 200",
            name="ck_product_ticket_title",
        ),
        CheckConstraint(
            "char_length(body) BETWEEN 1 AND 2000",
            name="ck_product_ticket_body",
        ),
        CheckConstraint(
            "ticket_kind IN ('report', 'triage', 'owner_ok', 'other')",
            name="ck_product_ticket_kind",
        ),
        Index("ix_product_ticket_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: wpis ticketu produktu — HITL, nie auto-fix / CAPA.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    ticket_code: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(String(2000), nullable=False)
    ticket_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
