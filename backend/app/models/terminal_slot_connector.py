import uuid
from datetime import time

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TerminalSlotConnector(Base, TimestampMixin):
    __tablename__ = "terminal_slot_connector"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_terminal_slot_connector_org_id"),
        UniqueConstraint(
            "organization_id",
            "connector_code",
            name="uq_terminal_slot_connector_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "terminal_code",
            name="uq_terminal_slot_connector_org_terminal",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_terminal_slot_connector_org_source_ref",
        ),
        CheckConstraint(
            "connector_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_terminal_slot_connector_code",
        ),
        CheckConstraint(
            "terminal_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_terminal_slot_connector_terminal",
        ),
        CheckConstraint(
            "mode IN ('api','email_hitl','portal_task','unsupported')",
            name="ck_terminal_slot_connector_mode",
        ),
        Index("ix_terminal_slot_connector_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: capability slotu tego tenanta — mode i godziny to dane, nie live N4.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    connector_code: Mapped[str] = mapped_column(String(32), nullable=False)
    terminal_code: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    opens_local: Mapped[time] = mapped_column(Time, nullable=False)
    closes_local: Mapped[time] = mapped_column(Time, nullable=False)
    cutoff_local: Mapped[time] = mapped_column(Time, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
