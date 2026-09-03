from uuid import UUID

from app.domain.errors import InvalidMailDraft
from app.domain.rate_line import require_source_ref

_DRAFT = "draft"
_EXTRACT = "extraction_draft"
_BODY_MAX = 2048


def mail_draft_status() -> str:
    return _DRAFT


def mail_draft_extract_kind() -> str:
    return _EXTRACT


def require_mail_draft_source_ref(raw: object) -> str:
    return require_source_ref(raw)


def require_mail_draft_subject_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMailDraft("subject_kind musi być tekstem")
    token = raw.strip()
    if token != _EXTRACT:
        raise InvalidMailDraft("subject_kind: tylko extraction_draft")
    return token


def require_mail_draft_subject_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidMailDraft("subject_id musi być UUID")
    return raw


def require_mail_draft_body(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMailDraft("treść musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidMailDraft("treść jest obowiązkowa")
    if len(token) > _BODY_MAX:
        raise InvalidMailDraft("treść za długa")
    return token
