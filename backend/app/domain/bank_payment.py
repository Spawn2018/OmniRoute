from uuid import UUID

from app.domain.errors import InvalidBankPayment

_MAX_REF = 256
_FIXTURE = "fixture://bank-payment/"
_MANUAL = "tenant:manual"


def require_payment_invoice_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidBankPayment("sales_invoice_id musi być UUID")
    return raw


def require_payment_account_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidBankPayment("party_bank_account_id musi być UUID")
    return raw


def require_payment_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidBankPayment("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidBankPayment("wskazanie zapisu płatności")
    if len(token) > _MAX_REF:
        raise InvalidBankPayment("wskazanie zapisu płatności za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidBankPayment("obce wskazanie zapisu płatności")
    return token
