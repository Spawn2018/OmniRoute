import re

from app.domain.errors import InvalidDangerousGood, InvalidImdgClass

_UN_NUMBER_PATTERN = re.compile(r"^[0-9]{4}$")
_IMDG_CLASSES = frozenset(
    {
        "1",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.5",
        "1.6",
        "2.1",
        "2.2",
        "2.3",
        "3",
        "4.1",
        "4.2",
        "4.3",
        "5.1",
        "5.2",
        "6.1",
        "6.2",
        "7",
        "8",
        "9",
    },
)


def normalize_un_number(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidDangerousGood("numer UN musi być tekstem")
    token = raw.strip().upper()
    if token.startswith("UN"):
        token = token[2:].strip()
    if _UN_NUMBER_PATTERN.fullmatch(token) is None:
        raise InvalidDangerousGood("numer UN: 4 cyfry")
    return token


def normalize_imdg_class(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidImdgClass("klasa IMDG musi być tekstem")
    token = raw.strip()
    if token not in _IMDG_CLASSES:
        raise InvalidImdgClass("klasa IMDG spoza allowlisty")
    return token


def normalize_un_aliases(raw: list[str]) -> list[str]:
    unique: list[str] = []
    for item in raw:
        token = normalize_un_number(item)
        if token not in unique:
            unique.append(token)
    return unique
