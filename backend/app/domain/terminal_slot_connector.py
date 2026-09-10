import re
from datetime import datetime, time

from app.domain.errors import InvalidTerminalSlotConnector

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MODES = frozenset({"api", "email_hitl", "portal_task", "unsupported"})
_MAX_REF = 256
_FIXTURE = "fixture://terminal-slot-connector/"
_MANUAL = "tenant:manual"
_CLOCKS = ("%H:%M:%S", "%H:%M")


def _snake(raw: object, token: str) -> str:
    if type(raw) is not str:
        raise InvalidTerminalSlotConnector(f"{token} musi być tekstem")
    stamp = raw.strip()
    if _CODE.fullmatch(stamp) is None:
        raise InvalidTerminalSlotConnector(f"{token}: snake 2–32")
    return stamp


def require_connector_code(raw: object) -> str:
    return _snake(raw, "oznaczenie")


def require_terminal_code(raw: object) -> str:
    return _snake(raw, "terminal")


def require_slot_mode(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTerminalSlotConnector("tryb musi być tekstem")
    stamp = raw.strip().lower()
    if stamp not in _MODES:
        raise InvalidTerminalSlotConnector("tryb: allowlista HITL")
    return stamp


def _clock(raw: object, token: str) -> time:
    if type(raw) is bool or type(raw) is float:
        raise InvalidTerminalSlotConnector(f"{token}: nie float")
    if type(raw) is time:
        return time(raw.hour, raw.minute, raw.second)
    if type(raw) is str:
        stamp = raw.strip()
        for fmt in _CLOCKS:
            try:
                parsed = datetime.strptime(stamp, fmt)
            except ValueError:
                continue
            return parsed.time()
    raise InvalidTerminalSlotConnector(f"{token}: godzina lokalna HH:MM")


def require_gate_clock(raw: object) -> time:
    return _clock(raw, "godziny")


def require_cutoff_clock(raw: object) -> time:
    return _clock(raw, "odcięcie")


def require_slot_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTerminalSlotConnector("obce source_ref")
    stamp = raw.strip()
    if stamp != _MANUAL and not stamp.startswith(_FIXTURE):
        raise InvalidTerminalSlotConnector("obce wskazanie zapisu konektora slotu")
    if len(stamp) > _MAX_REF:
        raise InvalidTerminalSlotConnector("obce wskazanie zapisu konektora slotu za długie")
    return stamp
