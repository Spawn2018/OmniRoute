from app.domain.errors import InvalidDocumentChecklistRule

_INCOTERMS = frozenset(
    {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"},
)
_SIDES = frozenset({"import", "export"})
_MODES = frozenset({"ocean", "road", "rail", "air"})
_KINDS = frozenset(
    {"commercial_invoice", "packing_list", "bill_of_lading", "export_declaration"},
)


def require_checklist_incoterm(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentChecklistRule("incoterm musi być tekstem")
    token = raw.strip().upper()
    if token not in _INCOTERMS:
        raise InvalidDocumentChecklistRule("nieznany incoterm")
    return token


def require_checklist_trade_side(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentChecklistRule("trade_side musi być tekstem")
    token = raw.strip()
    if token not in _SIDES:
        raise InvalidDocumentChecklistRule("nieznana strona handlu")
    return token


def require_checklist_mode(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentChecklistRule("mode musi być tekstem")
    token = raw.strip()
    if token not in _MODES:
        raise InvalidDocumentChecklistRule("nieznany mode")
    return token


def require_checklist_document_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDocumentChecklistRule("document_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidDocumentChecklistRule("nieznany rodzaj dokumentu checklisty")
    return token


def require_blocks_dispatch(raw: object) -> bool:
    if type(raw) is not bool:
        raise InvalidDocumentChecklistRule("blocks_dispatch musi być flagą")
    return raw
