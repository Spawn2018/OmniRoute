from app.domain.errors import InvalidTableView

_ALLOWED = frozenset({"party", "country", "status"})
_DEFAULT = "party"


def default_mail_group_by() -> str:
    return _DEFAULT


def require_mail_group_by(raw: object) -> str:
    if raw is None:
        return _DEFAULT
    if type(raw) is not str:
        raise InvalidTableView("group_by musi być tekstem")
    token = raw.strip()
    if token == "":
        return _DEFAULT
    if token not in _ALLOWED:
        raise InvalidTableView("group_by spoza allowlisty")
    return token


def normalize_table_view_config(raw: dict[str, object]) -> dict[str, object]:
    config = dict(raw)
    if "group_by" not in config:
        return config
    config["group_by"] = require_mail_group_by(config["group_by"])
    return config
