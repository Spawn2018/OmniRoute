import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ImpactScenario(Base, TimestampMixin):
    __tablename__ = "impact_scenario"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_impact_scenario_org_id"),
        UniqueConstraint(
            "organization_id",
            "scenario_code",
            name="uq_impact_scenario_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_impact_scenario_org_source_ref",
        ),
        CheckConstraint(
            "scenario_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_impact_scenario_code",
        ),
        CheckConstraint(
            "char_length(btrim(chain_label)) BETWEEN 1 AND 64",
            name="ck_impact_scenario_chain_label",
        ),
        Index("ix_impact_scenario_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: scenariusz skutku HITL tego tenanta — etykieta, nie EBITDA SQL.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    scenario_code: Mapped[str] = mapped_column(String(32), nullable=False)
    chain_label: Mapped[str] = mapped_column(String(64), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
