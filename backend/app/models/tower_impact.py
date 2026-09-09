import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

_STAGE_SQL = "chain_stage IN ('stock','production','sales','ebitda')"
_PACT_SQL = "contract_data_status IN ('missing','recorded')"


class TowerImpact(Base, TimestampMixin):
    __tablename__ = "tower_impact"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tower_impact_org_id"),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tower_impact_org_source_ref",
        ),
        CheckConstraint(_STAGE_SQL, name="ck_tower_impact_stage"),
        CheckConstraint(_PACT_SQL, name="ck_tower_impact_pact"),
        Index("ix_tower_impact_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik łańcucha tego tenanta — HITL etap, nie silnik EBITDA.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    chain_stage: Mapped[str] = mapped_column(String(16), nullable=False)
    contract_data_status: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
