from uuid import UUID

from app.domain.errors import InvalidTenderTedNotice

_MAX_REF = 256
_MAX_NOTICE = 64
_MIN_NOTICE = 8
_FIXTURE = "fixture://tender-ted-notice/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderTedNotice("tender_id musi być UUID")
    return raw


def require_notice_number(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderTedNotice("ogłoszenie musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) < _MIN_NOTICE or len(token) > _MAX_NOTICE:
        raise InvalidTenderTedNotice("ogłoszenie TED: 8–64 znaki")
    if "://" in token:
        raise InvalidTenderTedNotice("ogłoszenie TED nie jest URL")
    if not any(ch.isdigit() for ch in token):
        raise InvalidTenderTedNotice("ogłoszenie TED bez numeru")
    return token


def require_ted_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderTedNotice("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderTedNotice("wskazanie zapisu ogłoszenia TED")
    if len(token) > _MAX_REF:
        raise InvalidTenderTedNotice("wskazanie zapisu ogłoszenia TED za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderTedNotice("obce wskazanie zapisu ogłoszenia TED")
    return token
