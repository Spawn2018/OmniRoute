import re

from app.domain.errors import InvalidTermsAiMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_TERMS_KINDS = frozenset({"draft", "clause", "accept", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://terms-ai-mark/"

def parse_terms_ai_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTermsAiMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidTermsAiMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidTermsAiMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _TERMS_KINDS:
        raise InvalidTermsAiMark("rodzaj: draft, clause, accept albo other")
    if type(origin) is not str:
        raise InvalidTermsAiMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidTermsAiMark("obce wskazanie zapisu znacznika Terms AI")
    if len(pointer) > 256:
        raise InvalidTermsAiMark("obce wskazanie zapisu znacznika Terms AI za długie")
    return slug, token, pointer
