import json
from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidPortData, InvalidSourceRef
from app.domain.port import (
    decode_function_flags,
    normalize_country_code,
    normalize_port_aliases,
    normalize_unlocode,
    parse_coordinates,
)
from app.repositories.geography.port_repository import PortRepository


@dataclass(frozen=True)
class UnlocodeRecord:
    unlocode: str
    name: str
    country_code: str
    coordinates: str
    functions: str
    aliases: tuple[str, ...]


def parse_unlocode_records(payload: str) -> list[UnlocodeRecord]:
    decoded = json.loads(payload)
    if not isinstance(decoded, list):
        raise InvalidPortData("zbiór UN/LOCODE musi być listą rekordów")
    return [_record(entry) for entry in decoded]


async def ingest_ports(
    session: AsyncSession,
    *,
    organization_id: UUID,
    records: list[UnlocodeRecord],
    source_ref: str,
) -> int:
    pin = source_ref.strip()
    if pin == "":
        raise InvalidSourceRef("ingest portów wymaga pinu źródła w source_ref")

    rows = [_row(record, organization_id=organization_id, source_ref=pin) for record in records]
    return await PortRepository(session).upsert_many(rows)


def _record(entry: Any) -> UnlocodeRecord:
    if not isinstance(entry, dict):
        raise InvalidPortData("rekord UN/LOCODE musi być obiektem")
    return UnlocodeRecord(
        unlocode=str(entry["unlocode"]),
        name=str(entry["name"]),
        country_code=str(entry["countryCode"]),
        coordinates=str(entry.get("coordinates", "")),
        functions=str(entry["functions"]),
        aliases=tuple(str(alias) for alias in entry.get("aliases", [])),
    )


def _row(
    record: UnlocodeRecord,
    *,
    organization_id: UUID,
    source_ref: str,
) -> dict[str, object]:
    flags = decode_function_flags(record.functions)
    latitude, longitude = parse_coordinates(record.coordinates)
    return {
        "id": uuid4(),
        "organization_id": organization_id,
        "unlocode": normalize_unlocode(record.unlocode),
        "name": record.name.strip(),
        "country_code": normalize_country_code(record.country_code),
        "lat": latitude,
        "lng": longitude,
        "is_seaport": "port" in flags,
        "function_flags": flags,
        "aliases": normalize_port_aliases(record.aliases),
        "is_official": True,
        "source_ref": source_ref,
    }
