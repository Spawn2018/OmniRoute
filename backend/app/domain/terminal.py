from app.domain.errors import InvalidTerminalData

_ISPS_MAX = 32


def normalize_isps_code(raw: str | None) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidTerminalData("kod ISPS musi być tekstem")
    token = raw.strip().upper()
    if token == "":
        return None
    if len(token) > _ISPS_MAX:
        raise InvalidTerminalData("kod ISPS: najwyżej 32 znaki")
    return token


def normalize_terminal_name(raw: str) -> str:
    if type(raw) is not str:
        raise InvalidTerminalData("nazwa terminalu musi być tekstem")
    label = " ".join(raw.split())
    if label == "":
        raise InvalidTerminalData("nazwa terminalu jest wymagana")
    return label


def normalize_operator_name(raw: str | None) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidTerminalData("operator terminalu musi być tekstem")
    label = " ".join(raw.split())
    if label == "":
        return None
    return label
