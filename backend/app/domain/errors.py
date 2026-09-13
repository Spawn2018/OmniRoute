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
    """Akceptacja, odrzucenie i PATCH tylko dla szkicu w statusie pending."""


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


class ExtractionCandidatesNotEditable(DomainError):
    """PATCH candidates tylko na szkicu rate_line."""


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


class InvalidTrackingConsent(DomainError):
    """BR2.2: HITL zgoda na sledzenie — nie kolumna na kontakcie / live poll."""


class InvalidTrackingEvent(DomainError):
    """Zdarzenie trackingu: kind z allowlisty i czas ze strefą — nie czas przybycia liczony."""


class InvalidShipmentDocument(DomainError):
    """Dokument zlecenia: kind z allowlisty i source_ref zapisu — nie bajty, nie kwota."""


class InvalidOperationalException(DomainError):
    """Wyjatek operacyjny: kind z allowlisty i source_ref zapisu — nie czas przybycia, nie kwota."""


class InvalidCargoClaim(DomainError):
    """Reklamacja ładunku: OS&D i terminy CMR — nie kwota, nie scoring, nie silnik dni."""


class InvalidFraudFlag(DomainError):
    """Flaga oszustwa: kind z allowlisty i source_ref zapisu — nie kwota, nie scoring osoby."""


class InvalidEdiMessage(DomainError):
    """Komunikat EDI: kind z allowlisty i source_ref zapisu — nie parser, nie kwota."""


class InvalidSalesLane(DomainError):
    """BR6.1: HITL korytarz sprzedazy — nie UN/LOCODE / pipeline / HubSpot."""


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


class InvalidShipperTenderMark(DomainError):
    """BR6.2: HITL tryb zaladowcy — nie druga tabela tender / auto-award / Alpega."""


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
    """Kontener ISO 6346 — VGM HITL, nie kalkulator."""


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


class InvalidConsignment(DomainError):
    """Przesyłka N1 na zleceniu — nie paczka, nie unique FTL."""


class InvalidPalletBalance(DomainError):
    """Saldo palet Chep/LPR na kontrahencie — nie giełda, nie depozyt."""


class InvalidDocumentTemplate(DomainError):
    """Szablon wydruku jako dane — nie PDF, nie etykieta sieci."""


class InvalidRateCard(DomainError):
    """Karta stawek: applies_when jako dane + Decimal — nie silnik WHEN."""


class InvalidChargeTemplate(DomainError):
    """Szablon opłat: kolekcja kodów + daty; nakładanie liczy baza."""


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


class InvalidTenderBidStance(DomainError):
    """Postawa G2.11: HITL bid/no-bid z source_ref — nie win/loss i nie auto-award."""


class InvalidTenderAwardReview(DomainError):
    """Przegląd G2.12: HITL cztery oczy z source_ref — nie auto-award i nie szyna A/Z/O."""


class InvalidTenderTedNotice(DomainError):
    """Ogłoszenie G2.13: HITL numer TED z source_ref — nie scrape i nie live HTTP."""


class InvalidTenderCarbonMark(DomainError):
    """Ślad G2.14: HITL declared/exempt z source_ref — nie kg i nie kalkulator."""


class InvalidLanePattern(DomainError):
    """Wzorzec G2.19: HITL para UN/LOCODE z source_ref — nie km i nie circle_sim."""


class InvalidKreptdLicence(DomainError):
    """Licencja G2.23: HITL numer KREPTD z source_ref — nie scrape i nie Citizen API."""


class InvalidMonitoringScheme(DomainError):
    """Schemat C7: HITL kod monitoringu z source_ref — nie SENT XML i nie PUESC."""


class InvalidPartyDocument(DomainError):
    """Dokument C8: HITL kind na party z source_ref — nie 409 i nie extract."""


class InvalidCashDiscount(DomainError):
    """Skonto F2: HITL kind na fakturze z source_ref — nie kwota i nie CAMT."""


class InvalidCarbonMethod(DomainError):
    """Metodyka C5: HITL GLEC/GHG + wersja z source_ref — nie kg i nie kalkulator."""


class InvalidPredictionLedger(DomainError):
    """Ledger B0b/V1: HITL przedział + CRPS/MAE jako dane — nie silnik i nie scoring osoby."""


class InvalidSuggestionLedger(DomainError):
    """Ledger AI1.0: HITL podpowiedź + reakcja — nie zapis LLM i nie CRPS liczone."""


class InvalidOutcomeLedger(DomainError):
    """Ledger AI1.1: HITL fakt Decimal — nie CRPS liczone i nie FK do podpowiedzi."""


class InvalidOutcomeKind(DomainError):
    """Słownik AI1.4: HITL kind_code bez CHECK — nie ledger i nie ENUM."""


class InvalidCounterfactualRun(DomainError):
    """Przebieg AI1.2: HITL etykiety scenariusza — nie silnik i nie kwota."""


class InvalidBenefitLedger(DomainError):
    """Ledger AI1.3: HITL method_label + Decimal — nie druga marża i nie SQL z charge."""


class InvalidSuggestionKind(DomainError):
    """Słownik AI1.4: HITL kind_code bez CHECK — nie ledger i nie ENUM."""


class InvalidAutonomyLevel(DomainError):
    """Słownik AI1.4: HITL level_code bez CHECK — nie FK klienta i nie ENUM."""


class InvalidWeatherObservation(DomainError):
    """Pogoda V2: HITL warunek + UN/LOCODE + czas — nie Open-Meteo i nie ETA."""


class InvalidFreeTimeClock(DomainError):
    """Zegar V3: HITL rodzaj + free_days — nie countdown i nie charge."""


class InvalidTelematicsConnector(DomainError):
    """Konektor V5: HITL reżim + dostawca — nie live GPS i nie sekrety."""


class InvalidTelematicsDevice(DomainError):
    """BR2.1: HITL urządzenie — nie parowanie / live poll."""


class InvalidTowerImpact(DomainError):
    """Impact V6: HITL etap łańcucha + status umowy — nie scoring osoby i nie EBITDA."""


class InvalidTwinMark(DomainError):
    """Bliźniak W1: HITL rodzaj 8 — nie fizyka i nie plan_snapshot."""


class InvalidTwinKind(DomainError):
    """Słownik AI1.4: HITL kind_code bez CHECK — nie twin_mark i nie ENUM."""


class InvalidWarRoomMark(DomainError):
    """Sala W2: HITL rodzaj incydentu — nie koalescencja i nie drugi czat."""


class InvalidMemoryEdge(DomainError):
    """Pamięć W3: HITL rodzaj krawędzi — nie wyszukiwanie i nie graf zdarzeń."""


class InvalidExecutiveMark(DomainError):
    """Zarząd W4: HITL rodzaj pytania — nie suma LLM i nie zdania z agregatów."""


class InvalidRankMark(DomainError):
    """Ranking W5: HITL oś zakupu — nie auto-award i nie paczka szkiców."""


class InvalidTaskTemplate(DomainError):
    """T5: HITL szablon zadania — nie instancja, nie matching i nie outbox."""


class InvalidPlanSnapshot(DomainError):
    """B0b: HITL wersja planu — nie silnik, nie kółka. FK trójki od 452.0."""


class InvalidCircleSim(DomainError):
    """G2.20: HITL kółko jako dane — nie silnik 500k i nie km."""


class InvalidLaneKm(DomainError):
    """G2.21: HITL km ładowny/pusty/dolot jako dane — nie Haversine i nie trip."""


class InvalidErpConnector(DomainError):
    """F9: HITL konektor Optima jako dane — nie live SOAP i nie sekrety."""


class InvalidFactoringConnector(DomainError):
    """BR5.0: HITL konektor faktoringu jako dane — nie live SMEO HTTP i nie sekrety."""


class InvalidTerminalSlotConnector(DomainError):
    """T8: HITL capability slotu + godziny N4 — nie booking i nie confirmed z formularza."""


class InvalidIdpConnector(DomainError):
    """S53: HITL konektor IdP (auth0) jako dane — nie login i nie live HTTP."""


class InvalidExchangeConnector(DomainError):
    """S55: HITL konektor giełdy (trans_eu) jako dane — nie live HTTP i nie SPA."""


class InvalidCustomerContract(DomainError):
    """CI9: HITL nagłówek + opaque blob present/absent — nie szyfr."""


class InvalidTenantContractKek(DomainError):
    """CI9: HITL znacznik owijki (password|kms) — nie klucz i nie materiał."""


class InvalidVisibilityConnector(DomainError):
    """CT7: HITL konektor widoczności (p44) jako dane — nie live HTTP i nie feed."""


class InvalidPurchaseOrder(DomainError):
    """CT1: HITL nagłówek zamówienia zakupu — nie linia SKU i nie ASN."""


class InvalidPoLine(DomainError):
    """CT1: HITL linia zamówienia zakupu — nie ASN i nie kwota."""


class InvalidAsn(DomainError):
    """CT1: HITL awizo wysyłki — nie live EDI i nie auto shipment."""


class InvalidRoutingGuide(DomainError):
    """CT4: HITL przewodnik routingu — nie 409 egzekucja."""


class InvalidOtifMark(DomainError):
    """CT3: HITL zakres OTIF — nie metryka % i nie scoring SQL."""


class InvalidSapConnector(DomainError):
    """CT6: HITL konektor SAP/Oracle — nie live SOAP i nie SQL do SAP."""


class InvalidCapaMark(DomainError):
    """CT12: HITL rodzaj QMS CAPA/8D — nie workflow."""


class InvalidSlaClause(DomainError):
    """CI1: HITL klauzula SLA — nie extract i nie kara SQL."""


class InvalidDelayForecast(DomainError):
    """CI4: HITL prognoza opóźnienia — nie wróżba punktowa."""


class InvalidRemediationOption(DomainError):
    """CI6: HITL opcja naprawy — nie kwota i nie S11 silnik."""


class InvalidImpactScenario(DomainError):
    """CI6: HITL scenariusz skutku — nie EBITDA SQL."""


class InvalidClauseNotice(DomainError):
    """CI3: HITL powiadomienie o klauzuli — nie 409 i nie auto-kara."""


class InvalidCalibrationMark(DomainError):
    """CI7: HITL znacznik gotowości próbki — nie MAE SQL."""


class InvalidCampaignMark(DomainError):
    """BR6.5: HITL kampania — nie lejek X7 / atrybucja live."""


class InvalidGroupageDispatcherMark(DomainError):
    """BR3.2: HITL dyspozytor drobnicy — nie silnik hubów."""


class InvalidRepairPlaybook(DomainError):
    """CI8: HITL playbook naprawy — nie auto-send S11."""


class InvalidSpendMark(DomainError):
    """CI2: HITL rodzaj wycieku spend — nie SQL FV vs charge."""


class InvalidPenaltyMark(DomainError):
    """CI5: HITL rodzaj naruszenia kary — nie kara SQL."""


class InvalidInterventionOutcome(DomainError):
    """CI7: HITL wynik interwencji — nie SQL saved."""


class InvalidCrmLead(DomainError):
    """G1: HITL lead CRM — nie cold-send."""


class InvalidCrmOpportunity(DomainError):
    """BR6.0: HITL okazja CRM — nie pipeline / activity / cold-send."""


class InvalidLcChecklist(DomainError):
    """G3: HITL checklista LC — nie bank due."""


class InvalidNctsDraft(DomainError):
    """G4: HITL szkic NCTS — nie PUESC."""


class InvalidOogMark(DomainError):
    """G5: HITL znacznik OOG — nie wymiary."""


class InvalidOogPermitMark(DomainError):
    """BR4.1: HITL zezwolenie OOG — nie wymiary Decimal / live urząd."""


class InvalidLclConsoleMark(DomainError):
    """BR4.2: HITL konsola LCL/CFS — nie live CFS / CBM."""


class InvalidNacMark(DomainError):
    """BR4.3: HITL NAC / agent nominowany — nie live NAC HTTP."""


class InvalidSilkCorridorMark(DomainError):
    """BR4.4: HITL Jedwabny Szlak — nie live CR Express / para UN/LOCODE."""


class InvalidPoFinancingMark(DomainError):
    """BR5.1: HITL PO Financing — nie FK purchase_order / nie wycena zapasu."""


class InvalidLoadPlanMark(DomainError):
    """G6: HITL znacznik planu załadunku — nie solver OR."""


class InvalidLoadOrderMark(DomainError):
    """BR3.1: HITL kolejność załadunku — nie solver / wymiary Decimal."""


class InvalidCmmsMark(DomainError):
    """G7: HITL znacznik CMMS — nie work_order."""


class InvalidLegalHoldMark(DomainError):
    """G8: HITL znacznik legal hold — nie eIDAS crypto."""


class InvalidCompanyMark(DomainError):
    """G10: HITL znacznik spółki — nie drugi tenant."""


class InvalidBondedMark(DomainError):
    """G11: HITL znacznik bonded — nie WMS."""


class InvalidFilingSchemeMark(DomainError):
    """G12: HITL schemat składania — nie SENT-UE."""


class InvalidEdiMapMark(DomainError):
    """G13: HITL mapa pól EDI — nie silent write."""


class InvalidAeoDossierMark(DomainError):
    """G14: HITL dossier AEO — nie party_document."""


class InvalidYardMark(DomainError):
    """G15: HITL yard/waga/EIR — nie live yard."""


class InvalidBillingMark(DomainError):
    """G16: HITL billing SaaS — nie live Stripe."""


class InvalidRegistryPollMark(DomainError):
    """EXP7.2: HITL poll rejestru — nie live scrape."""


class InvalidWorkingCapitalMark(DomainError):
    """EXP2.1: HITL working capital — nie DSO SQL."""


class InvalidMakeOrBuyMark(DomainError):
    """EXP2.2: HITL make-or-buy — nie silnik kosztu."""


class InvalidCostAllocationMark(DomainError):
    """EXP2.3: HITL cost allocation — nie allocation SQL."""


class InvalidCargoCoverMark(DomainError):
    """EXP2.4: HITL cargo cover — nie live insurance."""


class InvalidSanctionsMark(DomainError):
    """EXP2.5: HITL lista sankcji — nie live scrape."""


class InvalidSubcontractEdgeMark(DomainError):
    """EXP2.6: HITL krawędź podwykonawstwa — nie graf live."""


class InvalidScheduleExceptionMark(DomainError):
    """EXP2.7: HITL wyjątek harmonogramu — nie silnik schedule."""


class InvalidCutoffMark(DomainError):
    """EXP2.8: HITL cutoff rozdzielony — nie silnik cutoff."""


class InvalidTimeToFixMark(DomainError):
    """EXP2.9: HITL TIME-TO-FIX — nie silnik TTF."""


class InvalidWhatIfMark(DomainError):
    """EXP2.10: HITL what-if — nie silnik scenariusza."""


class InvalidCabotageMark(DomainError):
    """EXP2.11: HITL kabotaż — nie silnik / RTPD."""


class InvalidCombinedTransportMark(DomainError):
    """EXP2.12: HITL combined transport — nie silnik / Mobility Package."""


class InvalidFerryArt9Mark(DomainError):
    """EXP2.13: HITL ferry art. 9 — nie tacho / Driver Time Solver."""


class InvalidFerryBookingMark(DomainError):
    """BR4.0: HITL rezerwacja promu — nie live bilet / solver art. 9."""


class InvalidFuelAnomalyMark(DomainError):
    """EXP2.14: HITL karta/anomalia paliwa — nie live card / telemetry."""


class InvalidFleetCostMark(DomainError):
    """EXP2.15: HITL koszt floty — nie TCO SQL / CMMS silnik."""


class InvalidBinPackMark(DomainError):
    """EXP2.16: HITL bin-pack — nie solver OR / LLM-VRP."""


class InvalidPalletPoolMark(DomainError):
    """EXP2.17: HITL pula palet — nie giełda / depozyt."""


class InvalidECmrMark(DomainError):
    """EXP2.18: HITL e-CMR/eFTI — nie filer live / e-CMR HTTP."""


class InvalidEDeliveryMark(DomainError):
    """EXP2.19: HITL e-Doręczenia — nie PUDO HTTP / live."""


class InvalidEDoreczeniaMark(DomainError):
    """EXP2.19: HITL e_doreczenia_mark — nie live ADE / bajty PDF."""


class InvalidPeppolMark(DomainError):
    """EXP2.20: HITL Peppol/MPP — nie AS4 HTTP / live."""


class InvalidSidImportMark(DomainError):
    """EXP2.21: HITL import SID — nie SID HTTP / ICS2 live."""


class InvalidIntegrationHubMark(DomainError):
    """EXP2.22: HITL Integration Hub — nie live HTTP / Selenium."""


class InvalidWebhookOutboxMark(DomainError):
    """EXP2.23: HITL webhook outbox — nie live dispatch / Temporal."""


class InvalidPartnerExchangeMark(DomainError):
    """EXP2.24: HITL giełda partnerska — nie live Trans.eu / auto-post."""


class InvalidRegulatoryRadarMark(DomainError):
    """EXP2.25: HITL regulatory radar — nie scrape urzędów / live feed."""


class InvalidIsoNis2Mark(DomainError):
    """EXP2.26: HITL ISO/NIS2 ops — nie audyt live / certyfikat HTTP."""


class InvalidOffboardingMark(DomainError):
    """EXP2.28: HITL offboarding — nie wipe ciphertext / DELETE konta."""


class InvalidJitJisMark(DomainError):
    """EXP3.1: HITL JIT/JIS — nie WMS live / silnik JIT."""


class InvalidJobMetricMark(DomainError):
    """EXP4.21: HITL metryka jobu — nie scoring osoby / SQL job."""


class InvalidDemoGpsMark(DomainError):
    """EXP0.11: HITL demo GPS — nie live GPS / lat/lng."""


class InvalidDemoWipeMark(DomainError):
    """Demo-1: HITL demo_wipe_mark — nie live wipe / DELETE tenant data / kwota."""


class InvalidDemoSimMark(DomainError):
    """Demo-1b: HITL demo_sim_mark — nie live sim / generator 150 aut / kwota."""


class InvalidPoPlantMark(DomainError):
    """EXP3.0b: HITL po_plant_mark — nie live EDI / auto shipment / kwota."""


class InvalidPoSkuMark(DomainError):
    """EXP3.0c: HITL po_sku_mark — nie live EDI / auto shipment / kwota."""


class InvalidPoBatchMark(DomainError):
    """EXP3.0d: HITL po_batch_mark — nie live EDI / auto shipment / kwota."""


class InvalidUnSegregationMark(DomainError):
    """EXP0.9: HITL un_segregation_mark — nie solver OR / LLM-VRP / kwota."""


class InvalidDualLedgerMark(DomainError):
    """EXP0.10: HITL dual_ledger_mark — nie druga marża / SQL na charge / kwota."""


class InvalidNamedPlaceMark(DomainError):
    """EXP0.6: HITL named_place_mark — nie cytat ICC / mutacja wyceny / kwota."""


class InvalidSlotGuaranteeMark(DomainError):
    """EXP0.3: HITL slot_guarantee_mark — nie live T8 / confirmed / kwota."""


class InvalidFreightTermMark(DomainError):
    """EXP1: HITL freight_term_mark — nie kolumna shipment / kwota."""


class InvalidCustomerPoMark(DomainError):
    """EXP1: HITL customer_po_mark — nie purchase_order CT1 / kwota."""


class InvalidProfitCenterMark(DomainError):
    """EXP1: HITL profit_center_mark — nie kolumna shipment / kwota."""


class InvalidHighValueMark(DomainError):
    """EXP1: HITL high_value_mark — nie kolumna shipment / cargo_value."""


class InvalidPaymentTermsMark(DomainError):
    """EXP1: HITL payment_terms_mark — nie kolumna shipment / payment_terms_days."""


class InvalidLanguageCodeMark(DomainError):
    """EXP1: HITL language_code_mark — nie kolumna shipment / preferred_language party."""


class InvalidHaulierRoleMark(DomainError):
    """EXP1: HITL haulier_role_mark — nie FK party na shipment / cargo_value."""


class InvalidDiversionMark(DomainError):
    """EXP1: HITL diversion_mark — nie FK shipment / cargo_value."""


class InvalidSpotContractMark(DomainError):
    """EXP1: HITL spot_contract_mark — nie FK quotation / cargo_value."""


class InvalidBidDecisionMark(DomainError):
    """EXP1: HITL bid_decision_mark — nie kolumna quotation / auto-award."""


class InvalidQuoteCurrencyMark(DomainError):
    """EXP1: HITL quote_currency_mark — nie kolumna quotation / NBP."""


class InvalidQuoteValidityMark(DomainError):
    """EXP1: HITL quote_validity_mark — nie kolumna quotation / data ważności."""


class InvalidImpersonateGuardMark(DomainError):
    """EXP0.12: HITL impersonate≠unwrap — nie crypto / Auth0 live."""


class InvalidFuelCardMark(DomainError):
    """EXP2.14: HITL fuel card — nie live fuel / litry / anomaly SQL."""


class InvalidVdaOdetteMark(DomainError):
    """EXP3.2: HITL VDA/Odette — nie live EDI VDA / ZPL."""


class InvalidInventoryPositionMark(DomainError):
    """EXP3.3: HITL inventory position — nie WMS live / bilans SQL."""


class InvalidFairShareMark(DomainError):
    """EXP3.4: HITL fair share — nie allocation SQL / druga marża."""


class InvalidMqcMark(DomainError):
    """EXP3.5: HITL MQC — nie MQC SQL / qty float."""


class InvalidEccnMark(DomainError):
    """EXP3.6: HITL ECCN — nie ECCN live / license HTTP."""


class InvalidEur1AtrMark(DomainError):
    """EXP3.7: HITL EUR.1/ATR — nie EUR.1 live / ATR scrape."""


class InvalidPhytoAtaMark(DomainError):
    """EXP3.8: HITL phyto/ATA — nie phyto live / ATA scrape."""


class InvalidSwitchBlLoiMark(DomainError):
    """EXP3.9: HITL switch BL/LOI — nie switch BL live / LOI scrape."""


class InvalidAbandonedRtoMark(DomainError):
    """EXP3.10: HITL abandoned/RTO — nie abandoned live / RTO scrape."""


class InvalidGeneralAverageMark(DomainError):
    """EXP3.11: HITL general average — nie GA live / GA scrape."""


class InvalidTenderDeclineReason(DomainError):
    """EXP3.12: HITL tender decline — nie decline auto / RFP scrape."""


class InvalidDemandSnapshotMark(DomainError):
    """EXP3.13: HITL demand snapshot — nie demand SQL / auto-forecast."""


class InvalidCsrdMark(DomainError):
    """EXP3.14: HITL CSRD — nie kg / CSRD live filing."""


class InvalidAirRa3Mark(DomainError):
    """EXP4.1: HITL air RA3/lithium — nie IATA live / RA3 scrape."""


class InvalidRailCimMark(DomainError):
    """EXP4.2: HITL rail UIC/CIM/SMGS — nie rail live filing / CIM scrape."""


class InvalidRailUicMark(DomainError):
    """EXP4.2: HITL rail_uic_mark — nie live rail API / km / mapa."""


class InvalidOceanAllianceMark(DomainError):
    """EXP4.3: HITL ocean alliance/feeder — nie ocean live API / alliance scrape."""


class InvalidOceanFeederMark(DomainError):
    """EXP4.3b: HITL ocean_feeder_mark — nie live feeder / TEU / AIS."""


class InvalidReeferMark(DomainError):
    """EXP4.5: HITL reefer — nie reefer live API / reefer scrape."""


class InvalidChassisMark(DomainError):
    """EXP4.5b: HITL chassis_mark — nie live chassis pool / TEU / yard."""


class InvalidLineImpactMark(DomainError):
    """EXP3.3b: HITL line_impact_mark — nie SQL line impact / EBITDA / plant live."""


class InvalidThreeWayMark(DomainError):
    """EXP3.3c: HITL three_way_mark — nie tuple per strona / wspólny SELECT / kwota."""


class InvalidEmptyDepotMark(DomainError):
    """EXP4.6: HITL empty/depot — nie depot live API / scrape."""


class InvalidNvoccMark(DomainError):
    """EXP4.7: HITL NVOCC — nie nvocc live API / scrape."""


class InvalidMultiManningMark(DomainError):
    """EXP4.8: HITL multi-manning — nie tacho live / driver2 SQL."""


class InvalidPostingMark(DomainError):
    """EXP4.9: HITL posting — nie posting live / tacho DDD."""


class InvalidPositionEvent(DomainError):
    """BR2.0: HITL zdarzenie pozycji — nie live GPS / wspolrzedne / poll."""


class InvalidTachoOfficeMark(DomainError):
    """EXP4.10: HITL tacho office — nie tacho live / DDD parse."""


class InvalidTachoPlanMark(DomainError):
    """BR3.3: HITL tacho w planie — nie live DDD / solver godzin."""


class InvalidLezMark(DomainError):
    """EXP4.11: HITL LEZ/zakazy — nie LEZ live / mapa."""


class InvalidLabelParkingMark(DomainError):
    """EXP4.12: HITL LABEL parking — nie parking live / mapa."""


class InvalidAbSusMark(DomainError):
    """EXP4.13: HITL A/B+SUS — nie A/B live / scoring SUS."""


class InvalidTermsAiMark(DomainError):
    """EXP4.15: HITL Terms AI — nie terms live / CI blob."""


class InvalidFunnelMark(DomainError):
    """EXP4.14: HITL X7 lejek — nie funnel live / CRM attribution."""


class InvalidMailAcceptMark(DomainError):
    """EXP4.16: HITL Accept z maila — nie Graph live / auto-send."""


class InvalidRoleViewMark(DomainError):
    """EXP4.17: HITL widok roli — nie board T6 / mapa."""


class InvalidRagSopMark(DomainError):
    """EXP4.18: HITL zakres RAG — nie pgvector / wycena."""


class InvalidCopyBanMark(DomainError):
    """EXP4.19: HITL zakaz copy claimów — nie silnik banów / kwota."""


class InvalidErruMark(DomainError):
    """EXP4.20: HITL sprawdzenie ERRU — nie live ERRU / scoring."""


class InvalidMobileClientMark(DomainError):
    """Mob: HITL klient mobilny — nie Expo / EAS / kwota."""


class InvalidFreightAuditMark(DomainError):
    """CT10: HITL rodzaj audytu frachtu — nie druga marża."""


class InvalidCollaborationMark(DomainError):
    """CT11: HITL rola współpracy 3 stron — nie wspólny SELECT."""


class InvalidRoutingGuideEnforcement(DomainError):
    """CT4 leftover: HITL tryb egzekucji przewodnika — nie żywy 409."""


class RoutingGuideOffGuide(DomainError):
    """CT4 leftover: ASN poza przewodnikiem przy block_409 — nie shipment."""


class InvalidRoutingGuideMatch(DomainError):
    """CT4 leftover: HITL tryb dopasowania przewodnika — nie silnik."""


class InvalidRoutePlanMark(DomainError):
    """BR3.0: HITL znacznik planu trasy — nie Valhalla / VRP / km."""
