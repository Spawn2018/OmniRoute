import csv
from dataclasses import dataclass
from decimal import Decimal
from io import StringIO
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import DuplicateWpiCode, InvalidSourceRef, InvalidUnlocode
from app.domain.port import normalize_unlocode
from app.domain.wpi import (
    HARBOR_SIZES,
    HARBOR_TYPES,
    SHELTERS,
    parse_optional_depth_m,
    parse_optional_label,
    parse_optional_wpi_number,
)
from app.repositories.geography.port_repository import PortRepository

_UNLOCODE = "UN/LOCODE"
_WPI_NUMBER = "World Port Index Number"
_HARBOR_SIZE = "Harbor Size"
_HARBOR_TYPE = "Harbor Type"
_SHELTER = "Shelter Afforded"
_CHANNEL = "Channel Depth (m)"
_CARGO = "Cargo Pier Depth (m)"


@dataclass(frozen=True)
class WpiRecord:
    unlocode: str
    wpi_number: int | None
    harbor_size: str | None
    harbor_type: str | None
    shelter: str | None
    channel_depth_m: Decimal | None
    cargo_pier_depth_m: Decimal | None


def parse_wpi_records(payload: str) -> list[WpiRecord]:
    rows = csv.DictReader(StringIO(payload))
    records: list[WpiRecord] = []
    seen: set[str] = set()
    for entry in rows:
        record = _record(entry)
        if record is None:
            continue
        if record.unlocode in seen:
            raise DuplicateWpiCode(f"dwa wiersze WPI na kod {record.unlocode}")
        seen.add(record.unlocode)
        records.append(record)
    return records


async def ingest_wpi(
    session: AsyncSession,
    *,
    organization_id: UUID,
    records: list[WpiRecord],
    source_ref: str,
) -> int:
    _ = organization_id
    pin = source_ref.strip()
    if pin == "":
        raise InvalidSourceRef("ingest WPI wymaga pinu źródła w wpi_source_ref")

    ports = PortRepository(session)
    updated = 0
    for record in records:
        applied = await ports.apply_wpi(
            record.unlocode,
            wpi_number=record.wpi_number,
            harbor_size=record.harbor_size,
            harbor_type=record.harbor_type,
            shelter=record.shelter,
            channel_depth_m=record.channel_depth_m,
            cargo_pier_depth_m=record.cargo_pier_depth_m,
            wpi_source_ref=pin,
        )
        if applied:
            updated += 1
    return updated


def _record(entry: dict[str, str]) -> WpiRecord | None:
    raw_code = entry.get(_UNLOCODE, "").strip()
    if raw_code == "":
        return None
    try:
        unlocode = normalize_unlocode(raw_code)
    except InvalidUnlocode:
        return None
    return WpiRecord(
        unlocode=unlocode,
        wpi_number=parse_optional_wpi_number(entry.get(_WPI_NUMBER, "")),
        harbor_size=parse_optional_label(
            entry.get(_HARBOR_SIZE, ""),
            allowed=HARBOR_SIZES,
            field="harbor_size",
        ),
        harbor_type=parse_optional_label(
            entry.get(_HARBOR_TYPE, ""),
            allowed=HARBOR_TYPES,
            field="harbor_type",
        ),
        shelter=parse_optional_label(entry.get(_SHELTER, ""), allowed=SHELTERS, field="shelter"),
        channel_depth_m=parse_optional_depth_m(entry.get(_CHANNEL, ""), field="channel_depth_m"),
        cargo_pier_depth_m=parse_optional_depth_m(
            entry.get(_CARGO, ""),
            field="cargo_pier_depth_m",
        ),
    )
