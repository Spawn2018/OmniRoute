import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TenantContractKek(Base, TimestampMixin):
    __tablename__ = "tenant_contract_kek"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_tenant_contract_kek_org_id"),
        UniqueConstraint(
            "organization_id",
            "kek_code",
            name="uq_tenant_contract_kek_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_tenant_contract_kek_org_source_ref",
        ),
        CheckConstraint(
            "kek_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_tenant_contract_kek_code",
        ),
        CheckConstraint(
            "wrap_kind IN ('password', 'kms')",
            name="ck_tenant_contract_kek_wrap",
        ),
        Index("ix_tenant_contract_kek_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: znacznik owijki tego tenanta — wrap_kind to token, nie materiał.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    kek_code: Mapped[str] = mapped_column(String(32), nullable=False)
    wrap_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
