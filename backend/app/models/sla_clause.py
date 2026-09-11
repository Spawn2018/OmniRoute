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


class SlaClause(Base, TimestampMixin):
    __tablename__ = "sla_clause"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id", "customer_contract_id"],
            ["customer_contract.organization_id", "customer_contract.id"],
            name="fk_sla_clause_customer_contract",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "id", name="uq_sla_clause_org_id"),
        UniqueConstraint(
            "organization_id",
            "clause_code",
            name="uq_sla_clause_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_sla_clause_org_source_ref",
        ),
        CheckConstraint(
            "clause_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_sla_clause_code",
        ),
        CheckConstraint(
            "metric_kind IN ('otif', 'delay', 'damage', 'other')",
            name="ck_sla_clause_metric",
        ),
        CheckConstraint(
            "char_length(btrim(threshold_label)) BETWEEN 1 AND 128",
            name="ck_sla_clause_threshold",
        ),
        Index("ix_sla_clause_organization_id", "organization_id"),
        Index("ix_sla_clause_org_contract", "organization_id", "customer_contract_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: klauzula SLA HITL tego tenanta — nie extract i nie kara SQL.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    customer_contract_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    clause_code: Mapped[str] = mapped_column(String(32), nullable=False)
    metric_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    threshold_label: Mapped[str] = mapped_column(String(128), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
