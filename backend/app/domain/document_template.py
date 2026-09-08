import re

from app.domain.errors import InvalidDocumentTemplate

_KINDS = frozenset({"own_label", "cmr"})
_LANGS = frozenset({"pl", "en"})
_OUTPUTS = frozenset({"html_print"})
_LAYOUT = re.compile(r"^[a-z0-9][a-z0-9_-]{1,63}$")
_MAX_REF = 256
_FIXTURE = "fixture://document-template/"
_MANUAL = "tenant:manual"


def require_template_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentTemplate("rodzaj szablonu musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidDocumentTemplate("nieznany rodzaj szablonu")
    return token


def require_layout_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentTemplate("układ szablonu musi być tekstem")
    token = raw.strip()
    if _LAYOUT.fullmatch(token) is None:
        raise InvalidDocumentTemplate("układ szablonu: 2–64 snake")
    return token


def require_template_language(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentTemplate("język szablonu musi być tekstem")
    token = raw.strip()
    if token not in _LANGS:
        raise InvalidDocumentTemplate("nieznany język szablonu")
    return token


def require_output_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentTemplate("wyjście szablonu musi być tekstem")
    token = raw.strip()
    if token not in _OUTPUTS:
        raise InvalidDocumentTemplate("nieznane wyjście szablonu")
    return token


def require_template_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentTemplate("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidDocumentTemplate("wskazanie zapisu szablonu")
    if len(token) > _MAX_REF:
        raise InvalidDocumentTemplate("wskazanie zapisu szablonu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidDocumentTemplate("obce wskazanie zapisu szablonu")
    return token
