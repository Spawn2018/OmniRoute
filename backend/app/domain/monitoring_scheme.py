import re

from app.domain.errors import InvalidMonitoringScheme

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://monitoring-scheme/"
_MANUAL = "tenant:manual"


def require_scheme_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMonitoringScheme("schemat musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidMonitoringScheme("schemat: snake 2–32")
    return token


def require_scheme_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMonitoringScheme("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidMonitoringScheme("wskazanie zapisu schematu monitoringu")
    if len(token) > _MAX_REF:
        raise InvalidMonitoringScheme("wskazanie zapisu schematu monitoringu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidMonitoringScheme("obce wskazanie zapisu schematu monitoringu")
    return token
