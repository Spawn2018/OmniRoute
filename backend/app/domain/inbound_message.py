from app.domain.errors import InvalidInboundMessage
from app.domain.rate_line import require_source_ref

_DRAFT = "draft"
_FIXTURE_PREFIXES = ("fixture://", "synth://")
_FROM_MAX = 320
_SUBJECT_MAX = 512
_BODY_MAX = 65536


def inbound_draft_status() -> str:
    return _DRAFT


def require_inbound_source_ref(raw: object) -> str:
    origin = require_source_ref(raw)
    if not origin.startswith(_FIXTURE_PREFIXES):
        raise InvalidInboundMessage("source_ref: fixture:// albo synth:// — nie IMAP")
    return origin


def require_from_address(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidInboundMessage("nadawca musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidInboundMessage("nadawca jest obowiązkowy")
    if " " in token or token.count("@") != 1:
        raise InvalidInboundMessage("nadawca: jeden adres e-mail")
    local, _, domain = token.partition("@")
    if local == "" or domain == "" or "." not in domain:
        raise InvalidInboundMessage("nadawca: jeden adres e-mail")
    if len(token) > _FROM_MAX:
        raise InvalidInboundMessage("nadawca za długi")
    return token.lower()


def require_subject(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidInboundMessage("temat musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidInboundMessage("temat jest obowiązkowy")
    if len(token) > _SUBJECT_MAX:
        raise InvalidInboundMessage("temat za długi")
    return token


def require_body_text(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidInboundMessage("treść musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidInboundMessage("treść jest obowiązkowa")
    if len(token) > _BODY_MAX:
        raise InvalidInboundMessage("treść za długa")
    return token
