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


class InvalidExtractionDraft(DomainError):
    """draft_kind spoza rate_line / carrier_quote / tender_rfp — nie F10."""


class AcceptRequiresChannelQuote(DomainError):
    """Accept szkicu oferty bez party, lane, dnia albo kwoty."""


class QuotationGap(DomainError):
    """Brak bieżącej stawki do wyceny — luka, nie liczona w Pythonie."""


class IncompleteQuotationSnapshot(DomainError):
    """Nowa wycena wymaga POL, POD i kontrahenta — częściowy snapshot nie wchodzi."""


class InvalidQuotationBatch(DomainError):
    """Wycena wsadowa: 1–20 kodów, bez pustego wsadu."""


class InvalidQuotationIncoterm(DomainError):
    """Incoterm / wersja / strona poza allowlistą — nie cytat ICC."""


class QuotationNamedPlaceRequired(DomainError):
    """DAP/DDP bez named_place — konflikt, nie luźna miejscowość."""


class MissingQuotationPrefix(DomainError):
    """Nadanie numeru oferty wymaga prefiksu w organization_setting."""


class InvalidQuotationDocumentNumber(DomainError):
    """Prefiks albo numer oferty poza formatem — nie licznik w ustawieniach."""


class InvalidOrganizationSetting(DomainError):
    """Ustawienie tenanta poza allowlistą, sekret albo zła wartość."""


class UnknownParty(DomainError):
    """Token tax_id nie ma wpisu w katalogu party tenanta — luźna nazwa nie przechodzi."""


class UnknownEmailDomain(DomainError):
    """Domena z adresu nie ma wpisu w katalogu party_email_domain tenanta."""


class InvalidPartyData(DomainError):
    """Pole kontrahenta puste, NIP bez sumy, rola spoza allowlisty albo para kredytu rozjechana."""


class PartyConflict(DomainError):
    """Ten sam identyfikator biznesowy już stoi w katalogu tenanta."""

    def __init__(self, message: str, *, existing_party_id: object) -> None:
        super().__init__(message)
        self.existing_party_id = existing_party_id


class InvalidCommodityCode(DomainError):
    """Kod towarowy: 4–10 cyfr HS/CN — nie luźna nazwa."""


class UnknownCommodityCode(DomainError):
    """Token nie ma wpisu w katalogu commodity_code tenanta."""


class CommodityCodeConflict(DomainError):
    """Kod albo alias towaru już zajęty w katalogu tenanta."""


class InvalidCurrency(DomainError):
    """Waluta kursu NBP: ISO 4217, trzy litery A–Z — nie luźna nazwa."""


class InvalidNbpRate(DomainError):
    """Kurs NBP: mid Decimal dodatni, data dzienna — nie float."""


class UnknownNbpRate(DomainError):
    """Brak kursu NBP tabeli A dla waluty i dnia w katalogu tenanta."""


class NbpRateConflict(DomainError):
    """Kurs tej waluty na ten dzień już jest w katalogu tenanta."""


class InvalidDangerousGood(DomainError):
    """Numer UN: 4 cyfry — prefiks UN zbędny, nie luźna nazwa."""


class InvalidImdgClass(DomainError):
    """Klasa IMDG spoza allowlisty 1–9 z podziałem."""


class UnknownDangerousGood(DomainError):
    """Token nie ma wpisu w katalogu dangerous_good tenanta."""


class DangerousGoodConflict(DomainError):
    """Numer UN albo alias już zajęty w katalogu tenanta."""


class InvalidNetworkCode(DomainError):
    """Kod sieci: snake 2–32 (a-z, potem a-z0-9_) — nie luźna nazwa."""


class UnknownNetwork(DomainError):
    """Token nie ma wpisu w katalogu network tenanta."""


class NetworkConflict(DomainError):
    """Kod albo alias sieci już zajęty w katalogu tenanta."""


class UnknownNetworkMember(DomainError):
    """network_member_id nie wskazuje członka tego tenanta."""


class InvalidCarrierInquiry(DomainError):
    """Zapytanie do agenta: network_member_id UUID, status draft — nie HTTP."""


class InvalidInboundMessage(DomainError):
    """Wiadomość przychodząca: fixture source_ref, nadawca, temat, treść — nie IMAP."""


class CustomerRfqConflict(DomainError):
    """Ta wiadomość już ma zapytanie ofertowe w tenancie."""


class InvalidCustomerRfq(DomainError):
    """Zapytanie ofertowe: fixture source_ref i wiadomość tenanta — nie kwota."""


class ShipmentConflict(DomainError):
    """Ta wycena już ma zlecenie w tenancie."""


class InvalidShipment(DomainError):
    """Zlecenie: source_ref zapisu i wycena z kontrahentem — nie kwota."""


class InvalidTrackingEvent(DomainError):
    """Zdarzenie trackingu: kind z allowlisty i czas ze strefą — nie czas przybycia liczony."""


class InvalidShipmentDocument(DomainError):
    """Dokument zlecenia: kind z allowlisty i source_ref zapisu — nie bajty, nie kwota."""


class InvalidOperationalException(DomainError):
    """Wyjatek operacyjny: kind z allowlisty i source_ref zapisu — nie czas przybycia, nie kwota."""


class InvalidCargoClaim(DomainError):
    """Reklamacja ładunku: kind z allowlisty i source_ref zapisu — nie kwota, nie scoring."""


class InvalidFraudFlag(DomainError):
    """Flaga oszustwa: kind z allowlisty i source_ref zapisu — nie kwota, nie scoring osoby."""


class InvalidEdiMessage(DomainError):
    """Komunikat EDI: kind z allowlisty i source_ref zapisu — nie parser, nie kwota."""


class InvalidSalesInvoice(DomainError):
    """Faktura: kind z allowlisty i source_ref zapisu — nie KSeF, nie kwota."""


class InvalidQuoteInvoiceSettlement(DomainError):
    """Rozliczenie: para wycena+faktura i source_ref — nie kwota, nie druga marża."""


class InvalidBankPayment(DomainError):
    """Płatność: para faktura+rachunek i source_ref — nie kwota, nie SEPA."""


class InvalidMoneyCost(DomainError):
    """Koszt pieniądza: para płatność+kurs i source_ref — nie kwota, nie odsetki."""


class InvalidFxDifference(DomainError):
    """Różnica kursowa: para wycena+kurs i source_ref — nie kwota, nie przeliczenie."""


class InvalidCashFlow(DomainError):
    """Przepływ: para wycena+płatność i source_ref — nie kwota, nie odejmowanie."""


class InvalidCostToServe(DomainError):
    """Koszt obsługi: para SOP+wycena i source_ref — nie kwota, nie suma."""


class InvalidBookkeeping(DomainError):
    """Księgowość: para opłata+faktura i source_ref — nie kwota, nie JPK."""


class InvalidCollectiveInvoice(DomainError):
    """Zbiorcza FV: faktura+dodatkowe zlecenie i source_ref — nie kwota, nie paczka."""


class InvalidGdprRequest(DomainError):
    """Wniosek RODO: konto+rodzaj i source_ref — nie kasowanie wiersza, nie DPIA."""


class InvalidShipmentLeg(DomainError):
    """Odcinek: zlecenie+dwie lokalizacje lądowe i source_ref — nie mapa, nie ETA."""


class InvalidPartyScorecard(DomainError):
    """Wskaźnik karty poza zakresem albo nie jest Decimal — nie float, nie scoring osoby."""


class UnknownPartyScorecard(DomainError):
    """Brak karty wyników dla tego kontrahenta w tenancie."""


class InvalidCustomerSop(DomainError):
    """Kod SOP: snake 2–32, albo pusta treść — nie luźny tytuł."""


class UnknownCustomerSop(DomainError):
    """Procedura nie ma wpisu w katalogu customer_sop tenanta."""


class CustomerSopConflict(DomainError):
    """Kod SOP już zajęty u tego kontrahenta w tenancie."""


class CustomerSopAlreadyApproved(DomainError):
    """Zatwierdzonej procedury nie zatwierdza się drugi raz — nowa wersja = leftover."""


class InvalidPortSurcharge(DomainError):
    """Kod extra: snake 2–32, albo kwota/waluta/warunek poza katalogiem — nie marża."""


class UnknownPortSurcharge(DomainError):
    """Extra nie ma wpisu w katalogu port_surcharge tenanta."""


class PortSurchargeConflict(DomainError):
    """Kod extra już zajęty przy tym porcie w tenancie."""


class InvalidChannelQuote(DomainError):
    """Kwota/waluta/data oferty z kanału poza katalogiem — nie marża."""


class UnknownChannelQuote(DomainError):
    """Oferta nie ma wpisu w katalogu channel_quote tenanta."""


class ChannelQuoteConflict(DomainError):
    """Oferta na ten dzień i lane już istnieje u tego armatora."""


class UnknownCarrierProfile(DomainError):
    """Kontrahent nie ma carrier_profile — oferta z kanału wymaga profilu armatora."""


class InvalidCreditReview(DomainError):
    """Decyzja recenzji poza ok/hold/refuse albo data nie jest dniem — nie scoring."""


class UnknownCreditReview(DomainError):
    """Recenzja nie ma wpisu w katalogu credit_review tenanta."""


class CreditReviewConflict(DomainError):
    """Recenzja na ten dzień u tego kontrahenta już istnieje."""


class InvalidOperatorDecision(DomainError):
    """Szyna decyzji: kind, status albo subject_id — nie accept extractu."""


class OperatorDecisionConflict(DomainError):
    """Pending na ten subject już istnieje w tenancie."""


class InvalidOperatorNotice(DomainError):
    """Powiadomienie: kind, treść albo source_ref — nie filtr wycen."""


class InvalidTableView(DomainError):
    """Widok tabeli: group_by spoza allowlisty — nie nowa kolumna, nie wątek."""


class InvalidMailDraft(DomainError):
    """Szkic maila: kind, treść, adres albo status — nie czat, nie Graph HTTP."""


class InvalidEntityEvent(DomainError):
    """Zdarzenie podmiotu: kind, subject albo source_ref — nie ledger predykcji."""


class InvalidOutboxEvent(DomainError):
    """Outbox: kind albo source_ref — nie Temporal, nie konsument."""


class InvalidFieldCarryForward(DomainError):
    """Przeniesienie pola: klucz z allowlisty i tekst — nie kwota, nie overwrite."""


class InvalidDocumentChecklistRule(DomainError):
    """Reguła checklisty: trójka incoterm×strona×mode i rodzaj dokumentu — nie dispatch."""


class InvalidIncotermResponsibility(DomainError):
    """Macierz obowiązków: para incoterm×strona i role z allowlisty — nie cytat ICC."""


class InvalidShipmentStakeholder(DomainError):
    """Strona zlecenia: rola z allowlisty i party_id — nie dispatch, nie EXP1."""


class InvalidDocumentDispatchRule(DomainError):
    """Reguła adresata: trójka incoterm×strona×rodzaj → rola I2 — nie send."""


class InvalidBookingInstruction(DomainError):
    """Instrukcja bookingu: scope + rola I2 + status — nie HTTP armatora."""


class InvalidOrganizationCalendar(DomainError):
    """Dzien kalendarza tenanta: kraj ISO + dzien + holiday/working — nie +3 kalendarzowe."""


class InvalidStop(DomainError):
    """Punkt na zleceniu: kind + miejsce + strefa IANA — nie mapa."""


class InvalidResource(DomainError):
    """Katalog floty: pojazd / kierowca / naczepa — nie trip."""


class InvalidTrip(DomainError):
    """Przejazd: numer + status + opcjonalna flota — nie km."""


class InvalidContainer(DomainError):
    """Kontener ISO 6346 — nie VGM."""


class InvalidGroupageLine(DomainError):
    """Linia drobnicy: kod + dwa location + cutoff + TT + ISODOW — nie WMS."""


class InvalidShipmentPackage(DomainError):
    """Paczka na zleceniu: skan QR Omni + stop trasy — nie WMS."""


class InvalidDockAppointment(DomainError):
    """Awizacja doku: okno TIME na stop magazynu — nie WMS."""


class InvalidCodInstruction(DomainError):
    """Znacznik pobrania COD na zleceniu — nie kwota, nie Fala F."""


class InvalidGroupageTariff(DomainError):
    """Cennik drobnicy: próg wagi na strefie — nie silnik P1."""


class InvalidOceanBill(DomainError):
    """Konosament LCL: HBL/MBL na zleceniu — nie PDF, nie booking."""


class InvalidPalletBalance(DomainError):
    """Saldo palet Chep/LPR na kontrahencie — nie giełda, nie depozyt."""


class InvalidDocumentTemplate(DomainError):
    """Szablon wydruku jako dane — nie PDF, nie etykieta sieci."""


class InvalidRateCard(DomainError):
    """Karta stawek: applies_when jako dane + Decimal — nie silnik WHEN."""


class InvalidChargeTemplate(DomainError):
    """Szablon opłat: kolekcja kodów + daty jako dane — nie exclusion."""


class InvalidFuelIndex(DomainError):
    """Indeks FSC/BAF/CAF jako dane obok nbp_rate — nie mnożenie na charge."""


class InvalidLocalCharge(DomainError):
    """Dopłata lokalna THC/ISPS jako dane + Decimal — nie warning braków."""


class InvalidTenderQuote(DomainError):
    """Oferta przetargowa kupna: ważność + limit orderów — nie auto-award."""


class InvalidTender(DomainError):
    """Nagłówek przetargu G2.0: strona/rodzaj/status jako dane — nie auto-award."""


class InvalidTenderLot(DomainError):
    """Partia przetargu G2.1: kod na nagłówku — nie korytarz i nie kwota."""


class InvalidTenderLane(DomainError):
    """Korytarz przetargu G2.2: para UN/LOCODE na partii — nie runda i nie kwota."""


class InvalidTenderRound(DomainError):
    """Runda przetargu G2.3: numer na nagłówku — nie data room i nie kwota."""


class InvalidTenderDataRoom(DomainError):
    """Pokój danych G2.4: NDA na nagłówku — nie extract i nie kwota."""


class InvalidTenderMatrixCell(DomainError):
    """Komórka matrycy G2.5: kwota Decimal z P — nie LLM i nie druga marża."""


class InvalidTenderPlaybook(DomainError):
    """Playbook G2.6: twierdzenie z source_ref — nie extract RFP i nie kwota."""


class InvalidTenderWinLoss(DomainError):
    """Win/loss G2.7: wynik z source_ref — nie extract RFP i nie four-eyes."""


class InvalidTenderConsortiumMember(DomainError):
    """Konsorcjum G2.8: fotel z source_ref — nie extract RFP i nie TED."""


class InvalidTenderRfpIntake(DomainError):
    """Przyjęcie RFP G2.9: HITL z source_ref — nie zapis z LLM i nie auto-award."""


class InvalidTenderProspect(DomainError):
    """Prospekt G2.10: HITL outreach z source_ref — nie scrape i nie bid/no-bid."""
