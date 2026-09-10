import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CustomerContract(Base, TimestampMixin):
    __tablename__ = "customer_contract"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_customer_contract_org_id"),
        UniqueConstraint(
            "organization_id",
            "contract_code",
            name="uq_customer_contract_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_customer_contract_org_source_ref",
        ),
        CheckConstraint(
            "contract_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_customer_contract_code",
        ),
        CheckConstraint(
            "char_length(shipper_label) BETWEEN 1 AND 128",
            name="ck_customer_contract_shipper",
        ),
        CheckConstraint(
            "char_length(their_customer_label) BETWEEN 1 AND 128",
            name="ck_customer_contract_customer",
        ),
        Index("ix_customer_contract_organization_id", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        comment="RLS tenant — nagłówek umowy, nie treść",
    )
    contract_code: Mapped[str] = mapped_column(String(32), nullable=False)
    shipper_label: Mapped[str] = mapped_column(String(128), nullable=False)
    their_customer_label: Mapped[str] = mapped_column(String(128), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    blob_ciphertext: Mapped[bytes | None] = mapped_column(
        BYTEA,
        nullable=True,
        comment="HITL opaque fixture bytes — present/absent, nie szyfr",
    )

    @property
    def has_ciphertext(self) -> bool:
        return self.blob_ciphertext is not None
