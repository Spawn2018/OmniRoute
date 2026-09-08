import uuid

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class IncotermResponsibility(Base, TimestampMixin):
    __tablename__ = "incoterm_responsibility"
    __table_args__ = (
        CheckConstraint(
            "incoterm IN ('EXW','FCA','CPT','CIP','DAP','DPU','DDP','FAS','FOB','CFR','CIF')",
            name="ck_incoterm_responsibility_incoterm",
        ),
        CheckConstraint(
            "trade_side IN ('import', 'export')",
            name="ck_incoterm_responsibility_side",
        ),
        CheckConstraint(
            "export_clearance_role IN ("
            "'seller','buyer','omni_customs','origin_agent','client_customs')",
            name="ck_incoterm_responsibility_export_role",
        ),
        CheckConstraint(
            "import_clearance_role IN ("
            "'seller','buyer','omni_customs','origin_agent','client_customs')",
            name="ck_incoterm_responsibility_import_role",
        ),
        CheckConstraint(
            "main_carriage_booker IN ('seller', 'buyer')",
            name="ck_incoterm_responsibility_booker",
        ),
        CheckConstraint(
            "booking_scope <@ ARRAY['precarriage','ocean','oncarriage',"
            "'contact_exchange','none']::text[] AND cardinality(booking_scope) >= 1",
            name="ck_incoterm_responsibility_scope",
        ),
        Index(
            "ix_incoterm_responsibility_org_pair",
            "organization_id",
            "incoterm",
            "trade_side",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    incoterm: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    trade_side: Mapped[str] = mapped_column(String(6), nullable=False)
    export_clearance_role: Mapped[str] = mapped_column(String(16), nullable=False)
    import_clearance_role: Mapped[str] = mapped_column(String(16), nullable=False)
    main_carriage_booker: Mapped[str] = mapped_column(String(8), nullable=False)
    booking_scope: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("incoterm_responsibility.id", ondelete="RESTRICT"),
        nullable=True,
    )
