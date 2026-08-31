class DomainError(Exception):
    """Bazowy wyjątek domenowy — mapowany na HTTP w jednym miejscu."""


class TenantContextMissing(DomainError):
    """Brak organization_id w kontekście sesji DB (RLS)."""


class PermissionDenied(DomainError):
    """Brak uprawnienia OpenFGA — endpoint bez jawnej zgody = odmowa."""


class ResourceNotFound(DomainError):
    """Zasób nie istnieje w kontekście tenanta / właściciela."""


class DraftNotPending(DomainError):
    """Akceptacja/odrzucenie tylko dla szkicu w statusie pending."""


class UntrustedExtractionInput(DomainError):
    """Wejście odrzucone przez llm-guard zanim trafi do modelu."""


class ExtractionProviderUnavailable(DomainError):
    """Provider instructor bez klucza / nieznana wartość EXTRACTION_PROVIDER."""
