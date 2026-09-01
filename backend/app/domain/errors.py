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


class InvalidChargeCode(DomainError):
    """Token katalogu: 2–32 znaki A-Z, 0-9, _ — nie luźny string."""


class ChargeCodeConflict(DomainError):
    """Kod albo alias już zajęty w katalogu tenanta."""


class UnknownChargeCode(DomainError):
    """Token nie ma wpisu w katalogu charge_code tenanta."""


class InvalidUnlocode(DomainError):
    """Kod portu: 5 znaków UN/LOCODE — dwie litery kraju, trzy znaki miejsca."""


class InvalidPortToken(DomainError):
    """Token do rozwiązania nazwy portu musi być niepustym tekstem."""


class InvalidPortData(DomainError):
    """Pole rekordu UN/LOCODE nie da się zdekodować — klasyfikator albo pozycja."""


class UnknownPort(DomainError):
    """Token nie ma wpisu w katalogu port tenanta — luźna nazwa nie przechodzi."""


class AmbiguousPortToken(DomainError):
    """Alias wskazuje więcej niż jeden oficjalny port — wybór należy do człowieka."""


class PortConflict(DomainError):
    """UN/LOCODE już zajęty w katalogu tenanta."""


class InvalidLocationData(DomainError):
    """Pole lokalizacji puste albo rodzaj spoza unlocode / postal_zone / address."""


class InvalidPostalCode(DomainError):
    """Kod pocztowy po normalizacji musi zostać znakami A-Z i 0-9."""


class InvalidPostalRange(DomainError):
    """Zakres pocztowy: równa długość obu końców, początek nie po końcu."""


class PostalRangeOverlap(DomainError):
    """Zakres nachodzi na inny w tej samej strefie tenanta — baza odmawia."""


class UnknownPostalZone(DomainError):
    """Kod pocztowy nie trafia w żaden zakres tenanta — luźny string nie przechodzi."""


class NotAPostalZone(DomainError):
    """Zakres można dopiąć wyłącznie do lokalizacji kind = postal_zone."""


class LocationConflict(DomainError):
    """Kod strefy już zajęty w katalogu lokalizacji tenanta."""


class InvalidTerminalData(DomainError):
    """Nazwa terminalu pusta albo kod ISPS nie jest tekstem."""


class UnknownTerminal(DomainError):
    """Kod ISPS nie ma wpisu w katalogu terminal tenanta."""


class TerminalConflict(DomainError):
    """Kod ISPS albo nazwa przy porcie już zajęta w katalogu tenanta."""


class InvalidWpiData(DomainError):
    """Pole World Port Index spoza słownika NGA albo nie da się sparsować."""


class DuplicateWpiCode(DomainError):
    """Dwa wiersze WPI na ten sam UN/LOCODE — nie last-write-wins."""


class InvalidSourceRef(DomainError):
    """Stawka bez source_ref nie wchodzi do bazy (HC-03)."""


class RateLineAlreadySuperseded(DomainError):
    """Zmiana stawki to nowy wiersz; już zastąpionej nie rusza się drugi raz."""


class MixedCurrencyCharge(DomainError):
    """buy i sell na charge muszą mieć tę samą walutę — marża nie liczy kursu."""


class ChargeRateMismatch(DomainError):
    """rate_line na charge musi mieć ten sam charge_code."""


class AcceptRequiresRateLine(DomainError):
    """Accept HITL bez poprawnej stawki kupna — cała transakcja wraca (1.3)."""


class QuotationGap(DomainError):
    """Brak bieżącej stawki do wyceny — luka, nie liczona w Pythonie."""


class InvalidOrganizationSetting(DomainError):
    """Ustawienie tenanta poza allowlistą, sekret albo zła wartość."""


class UnknownParty(DomainError):
    """Token tax_id nie ma wpisu w katalogu party tenanta — luźna nazwa nie przechodzi."""


class InvalidPartyData(DomainError):
    """Pole kontrahenta puste, NIP bez sumy, rola spoza allowlisty albo para kredytu rozjechana."""
