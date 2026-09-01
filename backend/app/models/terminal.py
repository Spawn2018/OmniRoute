import uuid
from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Terminal(Base, TimestampMixin):
    __tablename__ = "terminal"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "port_id"],
            ["port.organization_id", "port.id"],
            name="fk_terminal_port",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["organization_id", "operator_party_id"],
            ["party.organization_id", "party.id"],
            name="fk_terminal_operator_party",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_terminal_org_id"),
        UniqueConstraint(
            "organization_id",
            "port_id",
            "name",
            name="uq_terminal_org_port_name",
        ),
        Index(
            "uq_terminal_org_isps",
            "organization_id",
            "isps_code",
            unique=True,
            postgresql_where=text("isps_code IS NOT NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Ten sam tenant co w złożonym fk_terminal_port — baza odrzuca port obcego orga.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    port_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    isps_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    operator_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    operator_party_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    lat: Mapped[Decimal | None] = mapped_column(Numeric(8, 6), nullable=True)
    lng: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
