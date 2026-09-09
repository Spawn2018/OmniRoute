import uuid
from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ChargeTemplate(Base, TimestampMixin):
    """Kolekcja kodów opłat z oknem dat.

    Kolumna `validity_span` i wykluczanie nakładek żyją wyłącznie w bazie
    (migracja 146): daterange z exclusion GiST, nie pętla w Pythonie.
    """

    __tablename__ = "charge_template"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_charge_template_org_id"),
        ForeignKeyConstraint(
            ["organization_id", "charge_code"],
            ["charge_code.organization_id", "charge_code.code"],
            name="fk_charge_template_charge_code",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "template_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_charge_template_code_snake",
        ),
        CheckConstraint(
            "charge_code ~ '^[A-Z0-9_]{2,32}$'",
            name="ck_charge_template_member_token",
        ),
        CheckConstraint(
            "valid_until >= valid_from",
            name="ck_charge_template_window",
        ),
        Index("ix_charge_template_org_code", "organization_id", "template_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: szablon opłat jednego tenanta — daty CHECK nie zastępują polityki.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    template_code: Mapped[str] = mapped_column(String(32), nullable=False)
    charge_code: Mapped[str] = mapped_column(String(32), nullable=False)
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
