class DomainError(Exception):
    """Bazowy wyjątek domenowy — mapowany na HTTP w jednym miejscu."""


class TenantContextMissing(DomainError):
    """Brak organization_id w kontekście sesji DB (RLS)."""


class PermissionDenied(DomainError):
    """Brak uprawnienia OpenFGA — endpoint bez jawnej zgody = odmowa."""
