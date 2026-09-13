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

_SNAKE = r"^[a-z][a-z0-9_]{1,31}$"


class CounterfactualRun(Base, TimestampMixin):
    __tablename__ = "counterfactual_run"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_counterfactual_run_org_id"),
        UniqueConstraint(
            "organization_id",
            "run_code",
            name="uq_counterfactual_run_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_counterfactual_run_org_source_ref",
        ),
        CheckConstraint(
            f"run_code ~ '{_SNAKE}'",
            name="ck_counterfactual_run_code",
        ),
        Index("ix_counterfactual_run_organization_id", "organization_id"),
        ForeignKeyConstraint(
            ["organization_id", "plan_snapshot_id"],
            ["plan_snapshot.organization_id", "plan_snapshot.id"],
            name="fk_counterfactual_run_snapshot",
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: przebieg what-if tego tenanta. Migawka ma FK RESTRICT (453.0).
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    run_code: Mapped[str] = mapped_column(String(32), nullable=False)
    plan_snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    baseline_label: Mapped[str] = mapped_column(String(256), nullable=False)
    levers_label: Mapped[str] = mapped_column(String(256), nullable=False)
    result_label: Mapped[str] = mapped_column(String(256), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
