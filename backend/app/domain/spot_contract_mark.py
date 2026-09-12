import re

from app.domain.errors import InvalidSpotContractMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"spot", "contract", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://spot-contract-mark/"


def parse_spot_contract_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSpotContractMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidSpotContractMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSpotContractMark("rodzaj transakcji musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSpotContractMark(
            "rodzaj transakcji: spot, contract albo other",
        )
    if type(origin) is not str:
        raise InvalidSpotContractMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidSpotContractMark(
            "obce wskazanie zapisu znacznika spot/contract",
        )
    if len(pointer) > 256:
        raise InvalidSpotContractMark(
            "obce wskazanie zapisu znacznika spot/contract za długie",
        )
    return slug, token, pointer
