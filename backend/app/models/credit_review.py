import uuid
from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CreditReview(Base, TimestampMixin):
    __tablename__ = "credit_review"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "party_id",
            "review_date",
            name="uq_credit_review_org_party_day",
        ),
        ForeignKeyConstraint(
            ["organization_id", "party_id"],
            ["party.organization_id", "party.id"],
            name="fk_credit_review_party",
            ondelete="RESTRICT",
        ),
        CheckConstraint("decision IN ('ok','hold','refuse')", name="ck_credit_review_decision"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id", ondelete="RESTRICT"),
        index=True,
    )
    party_id: Mapped[uuid.UUID] = mapped_column()
    review_date: Mapped[date] = mapped_column(Date)
    decision: Mapped[str] = mapped_column(String(8))
    note: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_ref: Mapped[str] = mapped_column(String(256))
