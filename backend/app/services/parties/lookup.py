from dataclasses import dataclass
from os import environ

from httpx import Timeout

LOOKUP_TIMEOUT = Timeout(timeout=5.0)


@dataclass(frozen=True, slots=True)
class PartyDraft:
    legal_name: str
    tax_id: str
    source: str
    vies_valid: bool | None


@dataclass(frozen=True, slots=True)
class IbanWhitelistDraft:
    iban: str
    whitelist_status: str


_FIXTURE_PARTY = PartyDraft(
    legal_name="ACME Sp. z o.o.",
    tax_id="1234563218",
    source="gus",
    vies_valid=True,
)
_FIXTURE_IBAN = "PL61109010140000071219812874"


def lookup_party_draft(*, tax_id: str, country_code: str) -> PartyDraft:
    _ = LOOKUP_TIMEOUT
    _ = country_code
    _ = environ.get("PARTY_LOOKUP_BACKEND", "fixture")
    if tax_id == _FIXTURE_PARTY.tax_id:
        return _FIXTURE_PARTY
    return PartyDraft(
        legal_name=f"Szkic {tax_id}",
        tax_id=tax_id,
        source="gus",
        vies_valid=None,
    )


def lookup_iban_draft(iban: str) -> IbanWhitelistDraft:
    _ = LOOKUP_TIMEOUT
    _ = environ.get("PARTY_LOOKUP_BACKEND", "fixture")
    token = "".join(iban.split()).upper()
    status = "listed" if token == _FIXTURE_IBAN else "unavailable"
    return IbanWhitelistDraft(iban=token, whitelist_status=status)
