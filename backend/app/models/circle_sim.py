import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CircleSim(Base, TimestampMixin):
    __tablename__ = "circle_sim"
    __table_args__ = (
        UniqueConstraint("organization_id", "id", name="uq_circle_sim_org_id"),
        UniqueConstraint(
            "organization_id",
            "sim_code",
            name="uq_circle_sim_org_code",
        ),
        UniqueConstraint(
            "organization_id",
            "source_ref",
            name="uq_circle_sim_org_source_ref",
        ),
        UniqueConstraint(
            "organization_id",
            "unload_unlocode",
            "load_unlocode",
            name="uq_circle_sim_org_pair",
        ),
        CheckConstraint(
            "sim_code ~ '^[a-z][a-z0-9_]{1,31}$'",
            name="ck_circle_sim_code",
        ),
        CheckConstraint(
            "unload_unlocode <> load_unlocode",
            name="ck_circle_sim_ends_differ",
        ),
        CheckConstraint(
            r"unload_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_circle_sim_unload_unlocode",
        ),
        CheckConstraint(
            r"load_unlocode ~ '^[A-Z]{2}[A-Z0-9]{3}$'",
            name="ck_circle_sim_load_unlocode",
        ),
        Index("ix_circle_sim_organization_id", "organization_id"),
        Index("ix_circle_sim_org_unload", "organization_id", "unload_unlocode"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # RLS: kółko tego tenanta — para UN/LOCODE to dane, nie resolve geography.
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False
    )
    sim_code: Mapped[str] = mapped_column(String(32), nullable=False)
    unload_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    load_unlocode: Mapped[str] = mapped_column(String(5), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
