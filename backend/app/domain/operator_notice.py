from app.domain.errors import InvalidOperatorNotice
from app.domain.rate_line import require_source_ref

_UNREAD = "unread"
_READ = "read"
_MANUAL = "manual"
_NO_REPLY = "no_reply"
_KINDS = frozenset({_MANUAL, _NO_REPLY})
_BODY_MAX = 512


def operator_notice_unread_status() -> str:
    return _UNREAD


def operator_notice_manual_kind() -> str:
    return _MANUAL


def operator_notice_no_reply_kind() -> str:
    return _NO_REPLY


def require_notice_source_ref(raw: object) -> str:
    return require_source_ref(raw)


def require_notice_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOperatorNotice("kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidOperatorNotice("kind spoza allowlisty")
    return token


def require_notice_body(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOperatorNotice("treść musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidOperatorNotice("treść jest obowiązkowa")
    if len(token) > _BODY_MAX:
        raise InvalidOperatorNotice("treść za długa")
    return token


def notice_after_read(current: str) -> str:
    if current not in {_UNREAD, _READ}:
        raise InvalidOperatorNotice("status: unread albo read")
    return _READ
