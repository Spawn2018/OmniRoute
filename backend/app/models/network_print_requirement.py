import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class NetworkPrintRequirement(Base, TimestampMixin):
    __tablename__ = "network_print_requirement"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "id",
            name="uq_network_print_requirement_org_id",
        ),
        UniqueConstraint(
            "organization_id",
            "requirement_code",
            name="uq_network_print_requirement_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_network_print_requirement_org_source_ref",
        ),
        CheckConstraint(
            "requirement_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_network_print_requirement_code",
        ),
        CheckConstraint(
            "char_length(btrim(network_label)) BETWEEN 1 AND 64",
            name="ck_network_print_requirement_label",
        ),
        Index(
            "ix_network_print_requirement_organization_id",
            "organization_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: wymóg wydruku sieci tego tenanta — katalog HITL, nie 409.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
    )
    requirement_code: Mapped[str] = mapped_column(String(32), nullable=False)
    network_label: Mapped[str] = mapped_column(String(64), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
