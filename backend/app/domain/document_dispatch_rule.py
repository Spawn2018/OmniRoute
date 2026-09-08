from app.domain.errors import InvalidDocumentDispatchRule

_INCOTERMS = frozenset(
    {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"},
)
_SIDES = frozenset({"import", "export"})
_KINDS = frozenset(
    {"commercial_invoice", "packing_list", "bill_of_lading", "export_declaration"},
)
_ROLES = frozenset(
    {
        "shipper",
        "consignee",
        "origin_agent",
        "dest_agent",
        "ocean_carrier",
        "omni_customs",
        "client_customs",
    },
)
_MAX_REF = 256
_FIXTURE = "fixture://document-dispatch-rule/"
_MANUAL = "tenant:manual"


def require_dispatch_incoterm(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentDispatchRule("incoterm musi być tekstem")
    token = raw.strip().upper()
    if token not in _INCOTERMS:
        raise InvalidDocumentDispatchRule("nieznany incoterm")
    return token


def require_dispatch_trade_side(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentDispatchRule("trade_side musi być tekstem")
    token = raw.strip()
    if token not in _SIDES:
        raise InvalidDocumentDispatchRule("nieznana strona handlu")
    return token


def require_dispatch_document_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentDispatchRule("document_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidDocumentDispatchRule("nieznany rodzaj dokumentu wysyłki")
    return token


def require_recipient_role(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentDispatchRule("recipient_role musi być tekstem")
    token = raw.strip()
    if token not in _ROLES:
        raise InvalidDocumentDispatchRule("nieznana rola adresata")
    return token


def require_dispatch_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentDispatchRule("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidDocumentDispatchRule("wskazanie zapisu adresata")
    if len(token) > _MAX_REF:
        raise InvalidDocumentDispatchRule("wskazanie zapisu adresata za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidDocumentDispatchRule("obce wskazanie zapisu adresata")
    return token
