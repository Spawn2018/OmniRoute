from urllib.parse import quote
from uuid import UUID

from app.domain.errors import InvalidMailDraft
from app.domain.rate_line import require_source_ref

_DRAFT = "draft"
_SENT = "sent"
_EXTRACT = "extraction_draft"
_INQUIRY = "carrier_inquiry"
_KINDS = frozenset({_EXTRACT, _INQUIRY})
_BODY_MAX = 2048
_TO_MAX = 320


def mail_draft_status() -> str:
    return _DRAFT


def mail_draft_sent_status() -> str:
    return _SENT


def mail_draft_extract_kind() -> str:
    return _EXTRACT


def mail_draft_inquiry_kind() -> str:
    return _INQUIRY


def require_mail_draft_source_ref(raw: object) -> str:
    return require_source_ref(raw)


def require_mail_draft_subject_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMailDraft("subject_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidMailDraft("subject_kind spoza allowlisty")
    return token


def require_mail_draft_subject_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidMailDraft("subject_id musi być UUID")
    return raw


def require_mail_draft_subject_ids(raw: object) -> list[UUID]:
    if type(raw) is not list or raw == []:
        raise InvalidMailDraft("batch wymaga listy subject_id")
    return [require_mail_draft_subject_id(item) for item in raw]


def require_mail_draft_body(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMailDraft("treść musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidMailDraft("treść jest obowiązkowa")
    if len(token) > _BODY_MAX:
        raise InvalidMailDraft("treść za długa")
    return token


def require_mail_draft_to_address(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMailDraft("adres musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidMailDraft("adres jest obowiązkowy")
    if " " in token or token.count("@") != 1:
        raise InvalidMailDraft("adres: jeden e-mail")
    local, _, domain = token.partition("@")
    if local == "" or domain == "" or "." not in domain:
        raise InvalidMailDraft("adres: jeden e-mail")
    if len(token) > _TO_MAX:
        raise InvalidMailDraft("adres za długi")
    return token.lower()


def mail_draft_mailto_href(to_address: str, body: str) -> str:
    return f"mailto:{to_address}?body={quote(body, safe='')}"
