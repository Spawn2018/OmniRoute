import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_REACTION_SQL = "reaction IN ('accept','modify','reject')"
_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"
_CHANGED_SQL = (
    "(reaction IN ('accept','reject') AND changed_to = 'none') "
    "OR (reaction = 'modify' AND changed_to <> 'none')"
)


class SuggestionLedger(Base, TimestampMixin):
    __tablename__ = "suggestion_ledger"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_suggestion_ledger_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_suggestion_ledger_org_source_ref",
        ),
        ForeignKeyConstraint(
            ["organization_id", "suggestion_kind"],
            ["suggestion_kind.organization_id", "suggestion_kind.kind_code"],
            name="fk_suggestion_ledger_kind",
            ondelete="RESTRICT",
        ),
        CheckConstraint(_REACTION_SQL, name="ck_suggestion_ledger_reaction"),
        CheckConstraint("interval_high >= interval_low", name="ck_suggestion_ledger_interval"),
        CheckConstraint(_CHANGED_SQL, name="ck_suggestion_ledger_changed"),
        CheckConstraint(
            f"target_bc ~ '{_SNAKE}'",
            name="ck_suggestion_ledger_target_bc",
        ),
        CheckConstraint(
            f"model_version ~ '{_SNAKE}'",
            name="ck_suggestion_ledger_model",
        ),
        CheckConstraint(
            f"prompt_version ~ '{_SNAKE}'",
            name="ck_suggestion_ledger_prompt",
        ),
        Index("ix_suggestion_ledger_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: ledger podpowiedzi tego tenanta — UUID encji jest daną, nie FK.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    target_bc: Mapped[str] = mapped_column(String(32), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    suggestion_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    interval_low: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    interval_high: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    model_version: Mapped[str] = mapped_column(String(32), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(32), nullable=False)
    reaction: Mapped[str] = mapped_column(String(16), nullable=False)
    changed_to: Mapped[str] = mapped_column(String(256), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
