from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidContainer

_MAX_REF = 256
_FIXTURE = "fixture://container/"
_MANUAL = "tenant:manual"
_ISO_LEN = 11
_TYPE_LEN = 4
_MAX_SEAL = 32
_MAX_VESSEL = 128
_MAX_MARK = 64
_MAX_BOOK = 64
_BL_KINDS = frozenset({"original", "seawaybill", "telex", "express"})
_VGM_METHODS = frozenset({"method1", "method2"})
_MAX_ORIGIN_H = 8760
_MAX_DEMURRAGE_DAYS = 3650
_FOUR = Decimal("0.0001")


def _iso6346_value(mark: str) -> int:
    if mark.isdigit():
        return int(mark)
    rank = ord(mark) - 55
    return rank + rank // 11


def _iso6346_check_digit(prefix: str) -> int:
    total = 0
    weight = 1
    for mark in prefix:
        total += _iso6346_value(mark) * weight
        weight *= 2
    return (total % 11) % 10


def require_container_no(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidContainer("container_no musi być tekstem")
    token = raw.strip().upper()
    if len(token) != _ISO_LEN:
        raise InvalidContainer("numer kontenera ISO 6346")
    owner = token[:4]
    serial = token[4:10]
    if not owner.isalpha() or not serial.isdigit() or not token[10].isdigit():
        raise InvalidContainer("numer kontenera ISO 6346")
    if _iso6346_check_digit(token[:10]) != int(token[10]):
        raise InvalidContainer("cyfra kontrolna ISO 6346")
    return token


def require_iso_size_type(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidContainer("iso_size_type musi być tekstem")
    token = raw.strip().upper()
    if len(token) != _TYPE_LEN:
        raise InvalidContainer("typ ISO kontenera")
    if not token[:2].isdigit() or not token[2].isalpha() or not token[3].isalnum():
        raise InvalidContainer("typ ISO kontenera")
    return token


def require_container_shipment_id(raw: object) -> UUID | None:
    if raw is None:
        return None
    if type(raw) is not UUID:
        raise InvalidContainer("wskazanie zlecenia musi być UUID")
    return raw


def require_carrier_party_id(raw: object) -> UUID | None:
    if raw is None:
        return None
    if type(raw) is not UUID:
        raise InvalidContainer("wskazanie armatora musi być UUID")
    return raw


def require_container_shipment_leg_id(raw: object) -> UUID | None:
    if raw is None:
        return None
    if type(raw) is not UUID:
        raise InvalidContainer("wskazanie odcinka musi być UUID")
    return raw


def require_container_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidContainer("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidContainer("wskazanie zapisu kontenera")
    if len(token) > _MAX_REF:
        raise InvalidContainer("wskazanie zapisu kontenera za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidContainer("obce wskazanie zapisu kontenera")
    return token


def require_seal_no_1(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("plomba kontenera musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_SEAL:
        raise InvalidContainer("plomba kontenera za długa")
    return token


def require_seal_no_2(raw: object) -> str | None:
    return require_seal_no_1(raw)


def require_seal_no_3(raw: object) -> str | None:
    return require_seal_no_1(raw)


def require_vessel_name(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("statek musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_VESSEL:
        raise InvalidContainer("statek za długi")
    return token


def require_voyage_no(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("rejs musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_SEAL:
        raise InvalidContainer("rejs za długi")
    return token


def require_container_remarks(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("uwaga kontenera musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_REF:
        raise InvalidContainer("uwaga kontenera za długa")
    return token


def require_cargo_description(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("ładunek kontenera musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_REF:
        raise InvalidContainer("ładunek kontenera za długi")
    return token


def require_packaging_code(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("opakowanie kontenera musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_SEAL:
        raise InvalidContainer("opakowanie kontenera za długie")
    return token


def require_pickup_terminal(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("terminal kontenera musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_SEAL:
        raise InvalidContainer("terminal kontenera za długi")
    return token


def require_return_terminal(raw: object) -> str | None:
    return require_pickup_terminal(raw)


def require_container_bl_kind(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("rodzaj listu kontenera musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if token not in _BL_KINDS:
        raise InvalidContainer("rodzaj listu kontenera nieznany")
    return token


def require_free_time_origin_h(raw: object) -> int | None:
    if raw is None:
        return None
    if type(raw) is bool or type(raw) is not int:
        raise InvalidContainer("godziny wolnego czasu muszą być liczbą całkowitą")
    if raw < 0:
        raise InvalidContainer("godziny wolnego czasu: nieujemne")
    if raw > _MAX_ORIGIN_H:
        raise InvalidContainer("godziny wolnego czasu: za dużo")
    return raw


def require_free_time_dest_h(raw: object) -> int | None:
    return require_free_time_origin_h(raw)


def require_demurrage_free_days(raw: object) -> int | None:
    return _require_dd_days(raw, "demurrage")


def require_detention_free_days(raw: object) -> int | None:
    return _require_dd_days(raw, "detention")


def require_mixed_dd_days(raw: object) -> int | None:
    return _require_dd_days(raw, "mixed")


def _require_dd_days(raw: object, label: str) -> int | None:
    if raw is None:
        return None
    if type(raw) is bool or type(raw) is not int:
        raise InvalidContainer(f"dni {label} muszą być liczbą całkowitą")
    if raw < 0:
        raise InvalidContainer(f"dni {label}: nieujemne")
    if raw > _MAX_DEMURRAGE_DAYS:
        raise InvalidContainer(f"dni {label}: za dużo")
    return raw


def require_si_cutoff_at(raw: object) -> datetime | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("si musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    try:
        parsed = datetime.fromisoformat(token.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidContainer("si: ISO-8601") from exc
    if parsed.tzinfo is None:
        raise InvalidContainer("si: brak strefy")
    return parsed


def require_booking_no(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("booking musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_BOOK:
        raise InvalidContainer("booking za długi")
    return token


def require_ams_cutoff_at(raw: object) -> datetime | None:
    try:
        return require_si_cutoff_at(raw)
    except InvalidContainer as exc:
        raise InvalidContainer(str(exc).replace("si", "ams", 1)) from exc


def require_cy_cutoff_at(raw: object) -> datetime | None:
    try:
        return require_si_cutoff_at(raw)
    except InvalidContainer as exc:
        raise InvalidContainer(str(exc).replace("si", "cy", 1)) from exc


def require_cfs_cutoff_at(raw: object) -> datetime | None:
    try:
        return require_si_cutoff_at(raw)
    except InvalidContainer as exc:
        raise InvalidContainer(str(exc).replace("si", "cfs", 1)) from exc


def require_last_survey_at(raw: object) -> datetime | None:
    try:
        return require_si_cutoff_at(raw)
    except InvalidContainer as exc:
        raise InvalidContainer(str(exc).replace("si", "survey", 1)) from exc


def require_vgm_cutoff_at(raw: object) -> datetime | None:
    try:
        return require_si_cutoff_at(raw)
    except InvalidContainer as exc:
        raise InvalidContainer(str(exc).replace("si", "vgm", 1)) from exc


def require_vgm_kg(raw: object) -> Decimal | None:
    return _require_positive_kg(raw, "vgm")


def require_tare_kg(raw: object) -> Decimal | None:
    return _require_positive_kg(raw, "tara")


def _require_positive_kg(raw: object, label: str) -> Decimal | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidContainer(f"{label} nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidContainer(f"{label} musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidContainer(f"{label} musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidContainer(f"{label} musi być dodatnia")
    return parsed.quantize(_FOUR)


def require_vgm_method(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("vgm musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if token not in _VGM_METHODS:
        raise InvalidContainer("vgm nieznany")
    return token


def require_container_ref_1(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidContainer("referencja kontenera musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_MARK:
        raise InvalidContainer("referencja kontenera za długa")
    return token


def require_container_ref_2(raw: object) -> str | None:
    return require_container_ref_1(raw)


def require_container_ref_3(raw: object) -> str | None:
    return require_container_ref_1(raw)


def require_container_ref_4(raw: object) -> str | None:
    return require_container_ref_1(raw)


def require_container_ref_5(raw: object) -> str | None:
    return require_container_ref_1(raw)


def require_container_reefer(raw: object) -> bool:
    if type(raw) is not bool:
        raise InvalidContainer("chłodniczy kontenera musi być flagą")
    return raw
