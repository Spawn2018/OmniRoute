import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WhatIfReplay(Base):
    __tablename__ = "what_if_replay"

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    run_code: Mapped[str] = mapped_column(String(32), nullable=False)
    baseline_label: Mapped[str] = mapped_column(String(256), nullable=False)
    levers_label: Mapped[str] = mapped_column(String(256), nullable=False)
    result_label: Mapped[str] = mapped_column(String(256), nullable=False)
    source_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    plan_snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    snapshot_code: Mapped[str] = mapped_column(String(32), nullable=False)
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    trip_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
