class DomainError(Exception):
    """Bazowy wyjątek domenowy — mapowany na HTTP w jednym miejscu."""


class TenantContextMissing(DomainError):
    """Brak organization_id w kontekście sesji DB (RLS)."""


class Unauthenticated(DomainError):
    """Brak albo nieważny token sesji — zanim OpenFGA."""


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


class DocumentParserUnavailable(DomainError):
    """Parser docling niedostępny albo nieznany EXTRACTION_PARSER."""


class UnparseableDocument(DomainError):
    """Bajty dokumentu nie dały się zamienić na tekst do ekstrakcji."""


class InvalidMoney(DomainError):
    """Kwota musi być Decimal z walutą ISO 4217 — nigdy float."""
